import React, {useRef, useState, useCallback} from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  Alert,
  ActivityIndicator,
  PanResponder,
  GestureResponderEvent,
} from 'react-native';
import Svg, {Path} from 'react-native-svg';
import {useDispatch, useSelector} from 'react-redux';
import {useNavigation} from '@react-navigation/native';
import {NativeStackNavigationProp} from '@react-navigation/native-stack';

import {AppDispatch, RootState} from '../store';
import {submitAnalysis} from '../store/slices/analysisSlice';
import {MainStackParamList} from '../navigation/MainNavigator';
import {captureCanvasAsBase64} from '../utils/canvas';

type Nav = NativeStackNavigationProp<MainStackParamList, 'Tabs'>;

interface Stroke {
  path: string;
  color: string;
  width: number;
}

const COLORS = ['#000000', '#2563eb', '#ef4444', '#16a34a', '#ea580c'];
const WIDTHS = [2, 4, 7];

export default function CanvasScreen() {
  const dispatch = useDispatch<AppDispatch>();
  const navigation = useNavigation<Nav>();
  const {user, accessToken} = useSelector((s: RootState) => s.auth);
  const {loading} = useSelector((s: RootState) => s.analysis);

  const [strokes, setStrokes] = useState<Stroke[]>([]);
  const [undoStack, setUndoStack] = useState<Stroke[][]>([]);
  const [color, setColor] = useState(COLORS[0]);
  const [strokeWidth, setStrokeWidth] = useState(WIDTHS[1]);
  const currentPath = useRef('');

  const panResponder = PanResponder.create({
    onStartShouldSetPanResponder: () => true,
    onMoveShouldSetPanResponder: () => true,
    onPanResponderGrant: (e: GestureResponderEvent) => {
      const {locationX, locationY} = e.nativeEvent;
      currentPath.current = `M${locationX},${locationY}`;
    },
    onPanResponderMove: (e: GestureResponderEvent) => {
      const {locationX, locationY} = e.nativeEvent;
      currentPath.current += ` L${locationX},${locationY}`;
      setStrokes(prev => {
        const updated = [...prev];
        if (updated.length > 0 && updated[updated.length - 1].path === currentPath.current.split(' ')[0]) {
          updated[updated.length - 1] = {path: currentPath.current, color, width: strokeWidth};
          return updated;
        }
        return [...updated, {path: currentPath.current, color, width: strokeWidth}];
      });
    },
    onPanResponderRelease: () => {
      if (currentPath.current) {
        setUndoStack(prev => [...prev, strokes]);
        currentPath.current = '';
      }
    },
  });

  const handleUndo = useCallback(() => {
    if (undoStack.length === 0) {return;}
    setStrokes(undoStack[undoStack.length - 1]);
    setUndoStack(prev => prev.slice(0, -1));
  }, [undoStack, strokes]);

  const handleClear = useCallback(() => {
    Alert.alert('전체 지우기', '캔버스를 초기화하시겠습니까?', [
      {text: '취소', style: 'cancel'},
      {
        text: '확인',
        style: 'destructive',
        onPress: () => {
          setUndoStack(prev => [...prev, strokes]);
          setStrokes([]);
        },
      },
    ]);
  }, [strokes]);

  const handleSubmit = useCallback(async () => {
    if (strokes.length === 0) {
      Alert.alert('알림', '먼저 풀이를 작성해주세요.');
      return;
    }
    if (!user || !accessToken) {return;}

    const imageBase64 = await captureCanvasAsBase64(strokes);
    const result = await dispatch(
      submitAnalysis({
        imageBase64,
        recognizedLatex: '',
        userId: user.id,
        grade: user.grade ?? 'middle_1',
        token: accessToken,
      }),
    );

    if (submitAnalysis.fulfilled.match(result)) {
      navigation.navigate('Feedback', {
        submissionId: result.payload.submission_id,
      });
    }
  }, [strokes, user, accessToken, dispatch, navigation]);

  return (
    <View style={styles.container}>
      <View style={styles.toolbar}>
        <View style={styles.colorRow}>
          {COLORS.map(c => (
            <TouchableOpacity
              key={c}
              style={[styles.colorDot, {backgroundColor: c}, color === c && styles.colorDotActive]}
              onPress={() => setColor(c)}
            />
          ))}
        </View>
        <View style={styles.widthRow}>
          {WIDTHS.map(w => (
            <TouchableOpacity
              key={w}
              style={[styles.widthBtn, strokeWidth === w && styles.widthBtnActive]}
              onPress={() => setStrokeWidth(w)}>
              <View style={[styles.widthDot, {width: w * 2, height: w * 2, borderRadius: w}]} />
            </TouchableOpacity>
          ))}
        </View>
        <TouchableOpacity style={styles.iconBtn} onPress={handleUndo}>
          <Text style={styles.iconText}>↩</Text>
        </TouchableOpacity>
        <TouchableOpacity style={styles.iconBtn} onPress={handleClear}>
          <Text style={styles.iconText}>🗑</Text>
        </TouchableOpacity>
      </View>

      <View style={styles.canvas} {...panResponder.panHandlers}>
        <Svg style={StyleSheet.absoluteFill}>
          {strokes.map((s, i) => (
            <Path
              key={i}
              d={s.path}
              stroke={s.color}
              strokeWidth={s.width}
              fill="none"
              strokeLinecap="round"
              strokeLinejoin="round"
            />
          ))}
        </Svg>
        {strokes.length === 0 && (
          <Text style={styles.placeholder}>여기에 수학 풀이를 써주세요</Text>
        )}
      </View>

      <TouchableOpacity
        style={[styles.submitBtn, loading && styles.submitBtnDisabled]}
        onPress={handleSubmit}
        disabled={loading}>
        {loading ? (
          <ActivityIndicator color="#fff" />
        ) : (
          <Text style={styles.submitBtnText}>AI 분석 요청</Text>
        )}
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {flex: 1, backgroundColor: '#fff'},
  toolbar: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: 12,
    paddingVertical: 8,
    backgroundColor: '#f9fafb',
    borderBottomWidth: 1,
    borderBottomColor: '#e5e7eb',
    gap: 8,
  },
  colorRow: {flexDirection: 'row', gap: 6},
  colorDot: {width: 22, height: 22, borderRadius: 11},
  colorDotActive: {borderWidth: 3, borderColor: '#2563eb'},
  widthRow: {flexDirection: 'row', gap: 4, marginLeft: 8},
  widthBtn: {
    width: 30,
    height: 30,
    borderRadius: 15,
    backgroundColor: '#e5e7eb',
    alignItems: 'center',
    justifyContent: 'center',
  },
  widthBtnActive: {backgroundColor: '#bfdbfe'},
  widthDot: {backgroundColor: '#374151'},
  iconBtn: {
    width: 34,
    height: 34,
    borderRadius: 8,
    backgroundColor: '#e5e7eb',
    alignItems: 'center',
    justifyContent: 'center',
  },
  iconText: {fontSize: 16},
  canvas: {
    flex: 1,
    backgroundColor: '#fffef7',
    borderWidth: 1,
    borderColor: '#e5e7eb',
    margin: 8,
    borderRadius: 8,
    overflow: 'hidden',
  },
  placeholder: {
    position: 'absolute',
    top: '45%',
    left: 0,
    right: 0,
    textAlign: 'center',
    color: '#d1d5db',
    fontSize: 16,
  },
  submitBtn: {
    margin: 12,
    backgroundColor: '#2563eb',
    borderRadius: 12,
    paddingVertical: 14,
    alignItems: 'center',
  },
  submitBtnDisabled: {backgroundColor: '#93c5fd'},
  submitBtnText: {color: '#fff', fontSize: 16, fontWeight: '600'},
});

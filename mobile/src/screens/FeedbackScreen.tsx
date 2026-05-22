import React from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  ActivityIndicator,
} from 'react-native';
import {useSelector} from 'react-redux';
import {NativeStackNavigationProp} from '@react-navigation/native-stack';

import {RootState} from '../store';
import {MainStackParamList} from '../navigation/MainNavigator';

type Props = {
  navigation: NativeStackNavigationProp<MainStackParamList, 'Feedback'>;
  route: {params: {submissionId: string}};
};

export default function FeedbackScreen({navigation}: Props) {
  const {current, loading} = useSelector((s: RootState) => s.analysis);

  if (loading) {
    return (
      <View style={styles.centered}>
        <ActivityIndicator size="large" color="#2563eb" />
        <Text style={styles.loadingText}>AI가 풀이를 분석 중입니다...</Text>
      </View>
    );
  }

  if (!current) {
    return (
      <View style={styles.centered}>
        <Text style={styles.errorText}>분석 결과를 불러올 수 없습니다.</Text>
      </View>
    );
  }

  return (
    <ScrollView style={styles.container}>
      <View style={[styles.resultBanner, current.is_correct ? styles.correct : styles.incorrect]}>
        <Text style={styles.resultIcon}>{current.is_correct ? '✅' : '❌'}</Text>
        <Text style={styles.resultText}>
          {current.is_correct ? '정답입니다!' : '오답입니다'}
        </Text>
      </View>

      {!current.is_correct && current.error_type && (
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>오류 유형</Text>
          <Text style={styles.errorType}>{current.error_type}</Text>
          {current.error_step != null && (
            <Text style={styles.errorStep}>오류 발생 단계: {current.error_step}단계</Text>
          )}
        </View>
      )}

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>AI 피드백</Text>
        <Text style={styles.feedback}>{current.feedback}</Text>
      </View>

      {current.correct_solution && (
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>정석 풀이</Text>
          <Text style={styles.solution}>{current.correct_solution}</Text>
        </View>
      )}

      {current.concept_tags && current.concept_tags.length > 0 && (
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>관련 개념</Text>
          <View style={styles.tags}>
            {current.concept_tags.map(t => (
              <Text key={t} style={styles.tag}>
                {t}
              </Text>
            ))}
          </View>
        </View>
      )}

      <TouchableOpacity
        style={styles.retryBtn}
        onPress={() => navigation.goBack()}>
        <Text style={styles.retryBtnText}>다시 풀기</Text>
      </TouchableOpacity>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {flex: 1, backgroundColor: '#f5f7ff'},
  centered: {flex: 1, justifyContent: 'center', alignItems: 'center'},
  loadingText: {marginTop: 16, color: '#6b7280', fontSize: 15},
  errorText: {color: '#ef4444'},
  resultBanner: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    padding: 24,
    gap: 12,
  },
  correct: {backgroundColor: '#dcfce7'},
  incorrect: {backgroundColor: '#fee2e2'},
  resultIcon: {fontSize: 32},
  resultText: {fontSize: 22, fontWeight: '700', color: '#111827'},
  section: {
    backgroundColor: '#fff',
    borderRadius: 12,
    margin: 12,
    marginTop: 0,
    padding: 16,
    elevation: 1,
  },
  sectionTitle: {
    fontSize: 14,
    fontWeight: '600',
    color: '#6b7280',
    marginBottom: 8,
    textTransform: 'uppercase',
  },
  errorType: {fontSize: 16, color: '#dc2626', fontWeight: '600'},
  errorStep: {fontSize: 14, color: '#6b7280', marginTop: 4},
  feedback: {fontSize: 15, color: '#374151', lineHeight: 22},
  solution: {fontSize: 15, color: '#374151', lineHeight: 22},
  tags: {flexDirection: 'row', flexWrap: 'wrap', gap: 6},
  tag: {
    fontSize: 13,
    color: '#2563eb',
    backgroundColor: '#eff6ff',
    paddingHorizontal: 10,
    paddingVertical: 4,
    borderRadius: 12,
  },
  retryBtn: {
    margin: 16,
    backgroundColor: '#2563eb',
    borderRadius: 12,
    paddingVertical: 14,
    alignItems: 'center',
  },
  retryBtnText: {color: '#fff', fontSize: 16, fontWeight: '600'},
});

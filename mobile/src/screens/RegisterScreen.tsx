import React, {useState} from 'react';
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  StyleSheet,
  ActivityIndicator,
  KeyboardAvoidingView,
  Platform,
  ScrollView,
} from 'react-native';
import {useDispatch, useSelector} from 'react-redux';
import {NativeStackNavigationProp} from '@react-navigation/native-stack';

import {AppDispatch, RootState} from '../store';
import {register} from '../store/slices/authSlice';
import {AuthStackParamList} from '../navigation/AuthNavigator';

type Props = {
  navigation: NativeStackNavigationProp<AuthStackParamList, 'Register'>;
};

const GRADES = ['middle_1', 'middle_2', 'middle_3', 'high_1', 'high_2', 'high_3'];
const GRADE_LABELS: Record<string, string> = {
  middle_1: '중1', middle_2: '중2', middle_3: '중3',
  high_1: '고1', high_2: '고2', high_3: '고3',
};

export default function RegisterScreen({navigation}: Props) {
  const dispatch = useDispatch<AppDispatch>();
  const {loading, error} = useSelector((s: RootState) => s.auth);

  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [displayName, setDisplayName] = useState('');
  const [grade, setGrade] = useState('middle_1');

  const handleRegister = () => {
    if (!email || !password) {return;}
    dispatch(register({email, password, displayName, grade}));
  };

  return (
    <KeyboardAvoidingView
      style={styles.container}
      behavior={Platform.OS === 'ios' ? 'padding' : undefined}>
      <ScrollView contentContainerStyle={styles.inner}>
        <TextInput
          style={styles.input}
          placeholder="이름 (선택)"
          value={displayName}
          onChangeText={setDisplayName}
        />
        <TextInput
          style={styles.input}
          placeholder="이메일"
          value={email}
          onChangeText={setEmail}
          autoCapitalize="none"
          keyboardType="email-address"
        />
        <TextInput
          style={styles.input}
          placeholder="비밀번호"
          value={password}
          onChangeText={setPassword}
          secureTextEntry
        />

        <Text style={styles.label}>학년</Text>
        <View style={styles.gradeRow}>
          {GRADES.map(g => (
            <TouchableOpacity
              key={g}
              style={[styles.gradeBtn, grade === g && styles.gradeBtnActive]}
              onPress={() => setGrade(g)}>
              <Text
                style={[
                  styles.gradeBtnText,
                  grade === g && styles.gradeBtnTextActive,
                ]}>
                {GRADE_LABELS[g]}
              </Text>
            </TouchableOpacity>
          ))}
        </View>

        {error ? <Text style={styles.error}>{error}</Text> : null}

        <TouchableOpacity
          style={styles.button}
          onPress={handleRegister}
          disabled={loading}>
          {loading ? (
            <ActivityIndicator color="#fff" />
          ) : (
            <Text style={styles.buttonText}>회원가입</Text>
          )}
        </TouchableOpacity>

        <TouchableOpacity onPress={() => navigation.goBack()}>
          <Text style={styles.link}>이미 계정이 있으신가요? 로그인</Text>
        </TouchableOpacity>
      </ScrollView>
    </KeyboardAvoidingView>
  );
}

const styles = StyleSheet.create({
  container: {flex: 1, backgroundColor: '#f5f7ff'},
  inner: {padding: 24, paddingTop: 40},
  input: {
    backgroundColor: '#fff',
    borderRadius: 12,
    borderWidth: 1,
    borderColor: '#e5e7eb',
    paddingHorizontal: 16,
    paddingVertical: 12,
    marginBottom: 12,
    fontSize: 16,
  },
  label: {fontSize: 14, color: '#374151', marginBottom: 8, fontWeight: '500'},
  gradeRow: {flexDirection: 'row', flexWrap: 'wrap', gap: 8, marginBottom: 16},
  gradeBtn: {
    paddingHorizontal: 14,
    paddingVertical: 8,
    borderRadius: 20,
    borderWidth: 1,
    borderColor: '#d1d5db',
    backgroundColor: '#fff',
  },
  gradeBtnActive: {backgroundColor: '#2563eb', borderColor: '#2563eb'},
  gradeBtnText: {color: '#374151', fontSize: 14},
  gradeBtnTextActive: {color: '#fff'},
  button: {
    backgroundColor: '#2563eb',
    borderRadius: 12,
    paddingVertical: 14,
    alignItems: 'center',
    marginTop: 8,
  },
  buttonText: {color: '#fff', fontSize: 16, fontWeight: '600'},
  error: {color: '#ef4444', textAlign: 'center', marginBottom: 8},
  link: {textAlign: 'center', color: '#2563eb', marginTop: 16, fontSize: 14},
});

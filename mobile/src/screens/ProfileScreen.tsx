import React from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
} from 'react-native';
import {useDispatch, useSelector} from 'react-redux';

import {AppDispatch, RootState} from '../store';
import {logout} from '../store/slices/authSlice';

export default function ProfileScreen() {
  const dispatch = useDispatch<AppDispatch>();
  const {user} = useSelector((s: RootState) => s.auth);
  const {history} = useSelector((s: RootState) => s.analysis);

  const correct = history.filter(h => h.is_correct).length;
  const accuracy = history.length > 0 ? Math.round((correct / history.length) * 100) : 0;

  return (
    <ScrollView style={styles.container}>
      <View style={styles.profileCard}>
        <View style={styles.avatar}>
          <Text style={styles.avatarText}>
            {(user?.display_name ?? user?.email ?? '?')[0].toUpperCase()}
          </Text>
        </View>
        <Text style={styles.name}>{user?.display_name ?? user?.email}</Text>
        <Text style={styles.grade}>{user?.grade ?? '학년 미설정'}</Text>
      </View>

      <View style={styles.statsRow}>
        <View style={styles.statCard}>
          <Text style={styles.statValue}>{history.length}</Text>
          <Text style={styles.statLabel}>총 풀이</Text>
        </View>
        <View style={styles.statCard}>
          <Text style={styles.statValue}>{correct}</Text>
          <Text style={styles.statLabel}>정답</Text>
        </View>
        <View style={styles.statCard}>
          <Text style={styles.statValue}>{accuracy}%</Text>
          <Text style={styles.statLabel}>정답률</Text>
        </View>
      </View>

      {history.length > 0 && (
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>최근 풀이 기록</Text>
          {history.slice(0, 10).map((h, i) => (
            <View key={i} style={styles.historyItem}>
              <Text style={styles.historyIcon}>{h.is_correct ? '✅' : '❌'}</Text>
              <Text style={styles.historyFeedback} numberOfLines={2}>
                {h.feedback}
              </Text>
            </View>
          ))}
        </View>
      )}

      <TouchableOpacity
        style={styles.logoutBtn}
        onPress={() => dispatch(logout())}>
        <Text style={styles.logoutBtnText}>로그아웃</Text>
      </TouchableOpacity>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {flex: 1, backgroundColor: '#f5f7ff'},
  profileCard: {
    alignItems: 'center',
    padding: 24,
    backgroundColor: '#fff',
    marginBottom: 12,
  },
  avatar: {
    width: 72,
    height: 72,
    borderRadius: 36,
    backgroundColor: '#2563eb',
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: 12,
  },
  avatarText: {fontSize: 30, color: '#fff', fontWeight: '700'},
  name: {fontSize: 20, fontWeight: '700', color: '#111827'},
  grade: {fontSize: 14, color: '#6b7280', marginTop: 4},
  statsRow: {
    flexDirection: 'row',
    marginHorizontal: 12,
    marginBottom: 12,
    gap: 8,
  },
  statCard: {
    flex: 1,
    backgroundColor: '#fff',
    borderRadius: 12,
    padding: 16,
    alignItems: 'center',
    elevation: 1,
  },
  statValue: {fontSize: 24, fontWeight: '700', color: '#2563eb'},
  statLabel: {fontSize: 12, color: '#6b7280', marginTop: 4},
  section: {
    backgroundColor: '#fff',
    borderRadius: 12,
    margin: 12,
    marginTop: 0,
    padding: 16,
  },
  sectionTitle: {fontSize: 16, fontWeight: '600', color: '#111827', marginBottom: 12},
  historyItem: {
    flexDirection: 'row',
    alignItems: 'flex-start',
    marginBottom: 10,
    gap: 8,
  },
  historyIcon: {fontSize: 18},
  historyFeedback: {flex: 1, fontSize: 14, color: '#4b5563', lineHeight: 20},
  logoutBtn: {
    margin: 16,
    borderRadius: 12,
    paddingVertical: 14,
    alignItems: 'center',
    borderWidth: 1,
    borderColor: '#ef4444',
  },
  logoutBtnText: {color: '#ef4444', fontSize: 16, fontWeight: '600'},
});

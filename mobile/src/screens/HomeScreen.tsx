import React, {useEffect} from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  ActivityIndicator,
} from 'react-native';
import {useDispatch, useSelector} from 'react-redux';
import {useNavigation} from '@react-navigation/native';
import {BottomTabNavigationProp} from '@react-navigation/bottom-tabs';

import {AppDispatch, RootState} from '../store';
import {fetchRecommended} from '../store/slices/problemsSlice';
import {MainTabParamList} from '../navigation/MainNavigator';

type Nav = BottomTabNavigationProp<MainTabParamList, 'Home'>;

export default function HomeScreen() {
  const dispatch = useDispatch<AppDispatch>();
  const navigation = useNavigation<Nav>();
  const {user, accessToken} = useSelector((s: RootState) => s.auth);
  const {recommended, loading} = useSelector((s: RootState) => s.problems);

  useEffect(() => {
    if (user && accessToken) {
      dispatch(fetchRecommended({userId: user.id, token: accessToken}));
    }
  }, [dispatch, user, accessToken]);

  return (
    <ScrollView style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.greeting}>
          안녕하세요, {user?.display_name ?? user?.email} 님!
        </Text>
        <Text style={styles.subtitle}>오늘의 수학 풀이를 시작해 볼까요?</Text>
      </View>

      <TouchableOpacity
        style={styles.startButton}
        onPress={() => navigation.navigate('Canvas')}>
        <Text style={styles.startButtonText}>✏️ 풀이 시작</Text>
      </TouchableOpacity>

      <Text style={styles.sectionTitle}>추천 문제</Text>
      {loading ? (
        <ActivityIndicator style={styles.loader} />
      ) : recommended.length === 0 ? (
        <Text style={styles.empty}>추천 문제가 없습니다.</Text>
      ) : (
        recommended.slice(0, 5).map(p => (
          <View key={p.id} style={styles.card}>
            <View style={styles.cardHeader}>
              <Text style={styles.cardTitle}>{p.title}</Text>
              <Text style={styles.badge}>{p.difficulty}</Text>
            </View>
            <Text style={styles.cardContent} numberOfLines={2}>
              {p.content}
            </Text>
            <View style={styles.tags}>
              {(p.concept_tags ?? []).slice(0, 3).map(t => (
                <Text key={t} style={styles.tag}>
                  {t}
                </Text>
              ))}
            </View>
          </View>
        ))
      )}
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {flex: 1, backgroundColor: '#f5f7ff'},
  header: {padding: 24, paddingBottom: 8},
  greeting: {fontSize: 22, fontWeight: 'bold', color: '#111827'},
  subtitle: {fontSize: 14, color: '#6b7280', marginTop: 4},
  startButton: {
    margin: 16,
    backgroundColor: '#2563eb',
    borderRadius: 16,
    paddingVertical: 18,
    alignItems: 'center',
  },
  startButtonText: {color: '#fff', fontSize: 18, fontWeight: '700'},
  sectionTitle: {
    fontSize: 18,
    fontWeight: '600',
    color: '#111827',
    marginHorizontal: 16,
    marginTop: 8,
    marginBottom: 12,
  },
  loader: {marginTop: 20},
  empty: {textAlign: 'center', color: '#9ca3af', marginTop: 16},
  card: {
    backgroundColor: '#fff',
    borderRadius: 12,
    marginHorizontal: 16,
    marginBottom: 12,
    padding: 16,
    shadowColor: '#000',
    shadowOpacity: 0.05,
    shadowRadius: 4,
    elevation: 2,
  },
  cardHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 6,
  },
  cardTitle: {fontSize: 15, fontWeight: '600', color: '#111827', flex: 1},
  badge: {
    fontSize: 12,
    color: '#2563eb',
    backgroundColor: '#eff6ff',
    paddingHorizontal: 8,
    paddingVertical: 2,
    borderRadius: 6,
    marginLeft: 8,
  },
  cardContent: {fontSize: 14, color: '#4b5563', lineHeight: 20},
  tags: {flexDirection: 'row', flexWrap: 'wrap', marginTop: 8, gap: 4},
  tag: {
    fontSize: 12,
    color: '#6b7280',
    backgroundColor: '#f3f4f6',
    paddingHorizontal: 8,
    paddingVertical: 2,
    borderRadius: 10,
  },
});

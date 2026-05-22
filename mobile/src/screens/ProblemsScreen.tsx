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
import {fetchProblems} from '../store/slices/problemsSlice';
import {MainTabParamList} from '../navigation/MainNavigator';

type Nav = BottomTabNavigationProp<MainTabParamList, 'Problems'>;

const DIFFICULTY_COLOR: Record<string, string> = {
  easy: '#16a34a',
  medium: '#d97706',
  hard: '#dc2626',
};

export default function ProblemsScreen() {
  const dispatch = useDispatch<AppDispatch>();
  const navigation = useNavigation<Nav>();
  const {accessToken} = useSelector((s: RootState) => s.auth);
  const {list, loading} = useSelector((s: RootState) => s.problems);

  useEffect(() => {
    if (accessToken) {
      dispatch(fetchProblems(accessToken));
    }
  }, [dispatch, accessToken]);

  return (
    <View style={styles.container}>
      <Text style={styles.title}>문제 목록</Text>
      {loading ? (
        <ActivityIndicator style={styles.loader} />
      ) : list.length === 0 ? (
        <Text style={styles.empty}>문제가 없습니다.</Text>
      ) : (
        <ScrollView showsVerticalScrollIndicator={false}>
          {list.map(p => (
            <TouchableOpacity
              key={p.id}
              style={styles.card}
              onPress={() => navigation.navigate('Canvas')}>
              <View style={styles.cardHeader}>
                <Text style={styles.cardTitle}>{p.title}</Text>
                <Text
                  style={[
                    styles.diffBadge,
                    {color: DIFFICULTY_COLOR[p.difficulty] ?? '#6b7280'},
                  ]}>
                  {p.difficulty}
                </Text>
              </View>
              <Text style={styles.cardContent} numberOfLines={3}>
                {p.content}
              </Text>
              <View style={styles.tags}>
                {(p.concept_tags ?? []).slice(0, 4).map(t => (
                  <Text key={t} style={styles.tag}>
                    {t}
                  </Text>
                ))}
              </View>
            </TouchableOpacity>
          ))}
        </ScrollView>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {flex: 1, backgroundColor: '#f5f7ff', paddingTop: 16},
  title: {
    fontSize: 22,
    fontWeight: 'bold',
    color: '#111827',
    marginHorizontal: 16,
    marginBottom: 12,
  },
  loader: {marginTop: 40},
  empty: {textAlign: 'center', color: '#9ca3af', marginTop: 40},
  card: {
    backgroundColor: '#fff',
    borderRadius: 12,
    marginHorizontal: 16,
    marginBottom: 12,
    padding: 16,
    elevation: 2,
    shadowColor: '#000',
    shadowOpacity: 0.05,
    shadowRadius: 4,
  },
  cardHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 6,
  },
  cardTitle: {fontSize: 15, fontWeight: '600', color: '#111827', flex: 1},
  diffBadge: {fontSize: 12, fontWeight: '500', marginLeft: 8},
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

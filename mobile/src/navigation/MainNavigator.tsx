import React from 'react';
import {createBottomTabNavigator} from '@react-navigation/bottom-tabs';
import {createNativeStackNavigator} from '@react-navigation/native-stack';

import HomeScreen from '../screens/HomeScreen';
import CanvasScreen from '../screens/CanvasScreen';
import ProblemsScreen from '../screens/ProblemsScreen';
import FeedbackScreen from '../screens/FeedbackScreen';
import ProfileScreen from '../screens/ProfileScreen';

export type MainTabParamList = {
  Home: undefined;
  Canvas: undefined;
  Problems: undefined;
  Profile: undefined;
};

export type MainStackParamList = {
  Tabs: undefined;
  Feedback: {submissionId: string};
};

const Tab = createBottomTabNavigator<MainTabParamList>();
const Stack = createNativeStackNavigator<MainStackParamList>();

function TabNavigator() {
  return (
    <Tab.Navigator>
      <Tab.Screen name="Home" component={HomeScreen} options={{title: '홈'}} />
      <Tab.Screen
        name="Canvas"
        component={CanvasScreen}
        options={{title: '풀이'}}
      />
      <Tab.Screen
        name="Problems"
        component={ProblemsScreen}
        options={{title: '문제'}}
      />
      <Tab.Screen
        name="Profile"
        component={ProfileScreen}
        options={{title: '내 학습'}}
      />
    </Tab.Navigator>
  );
}

export default function MainNavigator() {
  return (
    <Stack.Navigator>
      <Stack.Screen
        name="Tabs"
        component={TabNavigator}
        options={{headerShown: false}}
      />
      <Stack.Screen
        name="Feedback"
        component={FeedbackScreen}
        options={{title: 'AI 피드백'}}
      />
    </Stack.Navigator>
  );
}

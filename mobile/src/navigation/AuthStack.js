import React, { useState, useEffect } from "react";
import { createNativeStackNavigator } from "@react-navigation/native-stack";

import SignInScreen from "../screen/SignInScreen";
import ForgotPasswordScreen from "../screen/ForgotPasswordScreen";
import SignUpScreen from "../screen/SignUpScreen";

const Stack = createNativeStackNavigator();

export default function AuthStack() {
  const [isFirstLaunch, setIsFirstLaunch] = useState(null);
  let routeName;

  return (
    <Stack.Navigator initialRouteName={routeName}>
      <Stack.Screen
        name="Sign In"
        component={SignInScreen}
        options={({ route }) => ({
          headerTitleStyle: { color: "black" },
          headerBackTitleVisible: false,
          headerShown: false,
        })}
      />
      <Stack.Screen
        name="Sign Up"
        component={SignUpScreen}
        options={({ route }) => ({
          headerTitleStyle: { color: "black" },
          headerBackTitleVisible: false,
          headerShown: false,
        })}
      />
      <Stack.Screen
        name="Forgot Password"
        component={ForgotPasswordScreen}
        options={({ route }) => ({
          headerTitleStyle: { color: "black" },
          headerBackTitleVisible: false,
          headerShown: false,
        })}
      />
    </Stack.Navigator>
  );
}

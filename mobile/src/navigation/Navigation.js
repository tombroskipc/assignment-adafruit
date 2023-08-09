import React, { useState, useContext, useEffect } from "react";
import { NavigationContainer } from "@react-navigation/native";
import { SafeAreaProvider } from "react-native-safe-area-context";

import { AuthContext } from "../context/AuthProvider";

import AppStack from "./AppStack";
import AuthStack from "./AuthStack";
import SplashScreen from "../screen/SplashScreen";

export default function Navigation() {
  const { userToken, isLoading } = useContext(AuthContext);
  return (
    <SafeAreaProvider>
      <NavigationContainer>
        {isLoading ? (
          <SplashScreen />
        ) : userToken === null ? (
          <AuthStack />
        ) : (
          <AppStack />
        )}
      </NavigationContainer>
    </SafeAreaProvider>
  );
}

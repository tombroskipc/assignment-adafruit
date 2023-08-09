import { createBottomTabNavigator } from "@react-navigation/bottom-tabs";
import HomeScreenStack from "../screen/HomeScreen";
import StaticsScreen from "../screen/StaticsScreen";
import AntiTheftScreen from "../screen/AntiTheftScreen";
import SettingsScreen from "../screen/SettingsScreen";
import { MaterialCommunityIcons } from "react-native-vector-icons";

import { getFocusedRouteNameFromRoute } from "@react-navigation/native";

const Tab = createBottomTabNavigator();

export default function AppStack() {
  const getTabBarVisibility = (route) => {
    const routeName = getFocusedRouteNameFromRoute(route) ?? "";
    if (routeName === "Device") {
      return "none";
    }
    return "flex";
  };

  return (
    <Tab.Navigator>
      <Tab.Screen
        name="Home"
        component={HomeScreenStack}
        options={({ route }) => ({
          headerShown: false,
          tabBarStyle: { display: getTabBarVisibility(route) },
          tabBarIcon: ({ color, size }) => (
            <MaterialCommunityIcons
              name="home-lightbulb"
              color={color}
              size={size}
            />
          ),
        })}
      />
      <Tab.Screen
        name="Stats"
        component={StaticsScreen}
        options={({ route }) => ({
          tabBarIcon: ({ color, size }) => (
            <MaterialCommunityIcons
              name="chart-bar"
              color={color}
              size={size}
            />
          ),
        })}
      />
      <Tab.Screen
        name="Anti-Theft"
        component={AntiTheftScreen}
        options={({ route }) => ({
          tabBarIcon: ({ color, size }) => (
            <MaterialCommunityIcons name="cctv" color={color} size={size} />
          ),
        })}
      />
      <Tab.Screen
        name="Settings"
        component={SettingsScreen}
        options={({ route }) => ({
          tabBarIcon: ({ color, size }) => (
            <MaterialCommunityIcons name="cog" color={color} size={size} />
          ),
        })}
      />
    </Tab.Navigator>
  );
}

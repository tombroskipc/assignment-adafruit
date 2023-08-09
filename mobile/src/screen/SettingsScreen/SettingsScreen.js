import React, { useContext } from "react";
import { View, Text, StyleSheet } from "react-native";

import { AuthContext } from "../../context/AuthProvider";

import CustomButton from "../../components/CustomButton";

export default function SettingsScreen() {
  const { signOut } = useContext(AuthContext);

  const signOutPressed = () => {
    signOut();
  };

  return (
    <View style={styles.container}>
      <View>
        <CustomButton text={"Log Out"} onPress={signOutPressed} />
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
  },
});

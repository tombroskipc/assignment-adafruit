import React from "react";
import { View, Text, StyleSheet } from "react-native";

export default function StaticsScreen() {
  return (
    <View style={styles.container}>
      <Text>This is Statics Screens</Text>
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

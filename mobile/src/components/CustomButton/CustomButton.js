import { View, Text, StyleSheet, Pressable } from "react-native";
import React from "react";

import { height, width } from "../../utils/Dimension";

const CustomButton = ({
  onPress,
  text,
  disabled = false,
  type = "PRIMARY",
  bgColor,
  fgColor,
}) => {
  return (
    <Pressable
      onPress={onPress}
      style={[
        styles.container,
        styles[`container_${type}`],
        bgColor ? { backgroundColor: bgColor } : {},
      ]}
      disabled={disabled}
    >
      <Text
        style={[
          styles.text,
          styles[`text_${type}`],
          fgColor ? { color: fgColor } : {},
        ]}
      >
        {text}
      </Text>
    </Pressable>
  );
};

const styles = StyleSheet.create({
  container: {
    padding: 15,
    marginVertical: 5,
    alignItems: "center",
    borderRadius: 15,
  },

  container_PRIMARY: {
    width: "100%",
    backgroundColor: "#048EF2",
  },

  container_TERTIARY: {
    width: "100%",
    backgroundColor: "#2A2A37",
  },

  container_SMALL: {
    width: "45%",
    backgroundColor: "#048EF2",
  },

  container_SMALL_TERTIARY: {
    width: "45%",
    backgroundColor: "#686D76",
  },

  container_ROUND: {
    // height: 0.3 * width,
    // width: "30%",
    height: 150,
    width: 150,
    justifyContent: "center",
    borderRadius: 45,
    borderWidth: 1.5,
    padding: 5,
    margin: 5,
    backgroundColor: "#048EF2",
  },

  text: {
    fontWeight: "bold",
    color: "white",
  },

  text_TERTIARY: {
    color: "white",
  },

  text_GROUP: {
    color: "white",
  },

  text_ROUND: {
    color: "white",
    fontSize: 30,
    fontWeight: "bold",
  },
});

export default CustomButton;

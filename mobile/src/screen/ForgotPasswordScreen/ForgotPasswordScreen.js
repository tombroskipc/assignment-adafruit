import {
  StyleSheet,
  Text,
  View,
  SafeAreaView,
  TouchableOpacity,
} from "react-native";
import React from "react";

const ForgotPasswordScreen = ({ navigation }) => {
  const toSignInPressed = () => {
    navigation.navigate("Sign In");
  };
  return (
    <SafeAreaView style={styles.container}>
      <Text>Forgot Password Screen</Text>
      <View style={styles.toSignIn}>
        <TouchableOpacity
          style={styles.toSignInPressed}
          onPress={toSignInPressed}
        >
          <Text>Return to Sign In</Text>
        </TouchableOpacity>
      </View>
    </SafeAreaView>
  );
};

export default ForgotPasswordScreen;

const styles = StyleSheet.create({
  container: {
    flex: 1,
    alignItems: "center",
    justifyContent: "center",
    backgroundColor: "#FFFFFF",
    padding: 20,
  },
  toSignIn: {
    flexDirection: "row",
    justifyContent: "space-evenly",
    margin: 5,
    marginBottom: 10,
  },
  toSignInTitle: {
    alignItems: "center",
    backgroundColor: "#ffffff",
    padding: 5,
  },
  toSignInPressed: {
    alignItems: "center",
    backgroundColor: "#cce6ff",
    padding: 5,
  },
});

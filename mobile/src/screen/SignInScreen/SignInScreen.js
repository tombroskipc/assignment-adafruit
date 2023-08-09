import React, { useState, useContext } from "react";
import {
  Text,
  View,
  SafeAreaView,
  Image,
  StyleSheet,
  TouchableOpacity,
} from "react-native";

import { width, height } from "../../utils/Dimension";

import Logo from "../../../assets/logo.png";
import CustomInput from "../../components/CustomInput";
import CustomButton from "../../components/CustomButton";

import { AuthContext } from "../../context/AuthProvider";

export default function SignInScreen({ navigation }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const { signIn } = useContext(AuthContext);

  const onSignInPressed = () => {
    signIn({ username, password });
  };
  const onSignUpPressed = () => {
    navigation.navigate("Sign Up");
  };

  const onForgotPassWordPressed = () => {
    navigation.navigate("Forgot Password");
  };

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.logo}>
        <Image
          source={Logo}
          style={{ width: width, height: height * 0.5 }}
          resizeMode="contain"
        />
      </View>
      <View style={styles.titleContainer}>
        <Text style={styles.title}>Sign In</Text>
      </View>
      <View style={styles.inputGroup}>
        <CustomInput
          placeholder={"Username"}
          value={username}
          setValue={setUsername}
          secureTextEntry={false}
        />
        <CustomInput
          placeholder={"Password"}
          value={password}
          setValue={setPassword}
          secureTextEntry
        />
      </View>

      <View style={styles.buttonGroup}>
        <CustomButton text="Enter Your House" onPress={onSignInPressed} />
        <CustomButton
          text="New Resident"
          onPress={onSignUpPressed}
          type="TERTIARY"
        />
      </View>
      <View style={styles.forgotPassword}>
        <View style={styles.forgotPasswordTitle}>
          <Text>Forgot password?</Text>
        </View>
        <TouchableOpacity
          style={styles.forgotPasswordPressed}
          onPress={onForgotPassWordPressed}
        >
          <Text>Press Here</Text>
        </TouchableOpacity>
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    alignItems: "center",
    backgroundColor: "#FFFFFF",
    padding: 20,
  },
  logo: {
    flex: 1.5,
    flexDirection: "row",
    justifyContent: "center",
    alignContent: "center",
    alignItems: "center",
    height: "50%",
  },
  titleContainer: {
    flex: 0.25,
    justifyContent: "center",
    alignItems: "center",
    alignContent: "center",
    fontSize: 20,
  },
  title: {
    fontSize: 20,
    fontFamily: "Arial",
  },
  inputGroup: {
    flex: 0.75,
    width: "100%",
    alignContent: "center",
    alignItems: "center",
    justifyContent: "space-evenly",
  },
  buttonGroup: {
    flex: 0.75,
    width: "70%",
    alignContent: "center",
    justifyContent: "center",
    alignItems: "center",
    marginVertical: 15,
    padding: 10,
  },
  forgotPassword: {
    flexDirection: "row",
    justifyContent: "space-evenly",
    margin: 5,
    marginBottom: 10,
  },
  forgotPasswordTitle: {
    alignItems: "center",
    backgroundColor: "#ffffff",
    padding: 5,
  },
  forgotPasswordPressed: {
    alignItems: "center",
    backgroundColor: "#ffffff",
    padding: 5,
  },
});

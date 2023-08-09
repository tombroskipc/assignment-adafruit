import { StyleSheet, Text, View, SafeAreaView, Image } from "react-native";
import React, { useState, useContext } from "react";

import { width, height } from "../../utils/Dimension";

import Logo from "../../../assets/logo.png";
import CustomInput from "../../components/CustomInput";
import CustomButton from "../../components/CustomButton";

import { AuthContext } from "../../context/AuthProvider";

const SignUpScreen = ({ navigation }) => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const { signUp } = useContext(AuthContext);

  // const { height, width } = useWindowDimensions();

  const onSignUpPressed = () => {
    signUp({ username, password });
    navigation.navigate("Sign In");
  };

  const toSignInPressed = () => {
    navigation.navigate("Sign In");
  };
  return (
    <View style={styles.container}>
      <View style={styles.logo}>
        <Image
          source={Logo}
          style={{ width: width, height: height * 0.5 }}
          resizeMode="contain"
        />
      </View>
      <View style={styles.titleContainer}>
        <Text style={styles.title}>Sign Up</Text>
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
        <CustomButton
          text="Sign Up Now"
          onPress={onSignUpPressed}
          type="SMALL"
        />
        <CustomButton
          text="Return to Sign In"
          onPress={toSignInPressed}
          type="SMALL_TERTIARY"
        />
      </View>
    </View>
  );
};

export default SignUpScreen;

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
    flex: 0.9,
    flexDirection: "row",
    width: "100%",
    alignContent: "center",
    justifyContent: "space-evenly",
    alignItems: "center",
    marginVertical: 15,
    padding: 10,
    // backgroundColor: "#ff5050",
  },
});

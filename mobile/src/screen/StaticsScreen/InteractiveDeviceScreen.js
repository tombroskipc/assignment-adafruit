import React, { useState, useEffect, useContext } from "react";
import { View, SafeAreaView, Text, StyleSheet, FlatList } from "react-native";
import { useRoute } from "@react-navigation/native";
import axios from "axios";

import { AuthContext } from "../../context/AuthProvider";

import { baseURL } from "../../../env";

// import CustomButton from "../../components/CustomButton";
import { ThemedButton } from "react-native-really-awesome-button";
import { MaterialCommunityIcons } from "react-native-vector-icons";

import { deviceMode } from "../../utils/ObjectMap";

export default function InteractiveDeviceScreen() {
  const { userToken } = useContext(AuthContext);

  const route = useRoute();
  const [isFirstTime, setIsFisrtTime] = useState(true);
  const [value, setValue] = useState(route.params.curr_value);
  const [currentButton, setCurrentButon] = useState(
    deviceMode[route.params.type].key
  );

  useEffect(() => {
    putData();
  }, [value]);

  const form = new FormData();
  form.append("data", value);

  const putData = () => {
    if (isFirstTime === true) {
      setIsFisrtTime(false);
    } else {
      axios
        .put(`${baseURL}/api/v1/device/${route.params.device_id}`, form, {
          headers: {
            "access-token": userToken,
          },
        })
        .then(function (response) {
          // handle success
          console.log("InteractiveDevice: Send Data Successful!");
        })
        .catch(function (error) {
          // handle error
          alert(error.message);
        });
    }
  };

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.listContainer}>
        <FlatList
          data={deviceMode[route.params.type]}
          contentContainerStyle={styles.listContent}
          numColumns={2}
          scrollEnabled={false}
          keyExtractor={(item) => item.key}
          renderItem={({ item }) => (
            <ThemedButton
              name="bruce"
              type="primary"
              height={100}
              width={150}
              textSize={25}
              before={
                <MaterialCommunityIcons
                  name={item.icon}
                  color={item.key === currentButton ? "#625E5D" : "#FFFFFF"}
                  size={40}
                />
              }
              backgroundColor={item.color}
              disabled={item.key === currentButton ? true : false}
              onPress={() => {
                setValue(item.value);
                setCurrentButon(item.key);
                console.log("Sending", item.value, "...");
              }}
              style={styles.button}
            >
              {item.key}
            </ThemedButton>
          )}
        />
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    alignItems: "center",
  },
  listContent: {
    flex: 1,
    width: "100%",
    height: "100%",
    alignItems: "center",
    justifyContent: "center",
  },
  button: {
    margin: 10,
  },
});

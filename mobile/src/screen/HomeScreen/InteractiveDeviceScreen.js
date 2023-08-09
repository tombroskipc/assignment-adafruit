import React, { useState, useEffect, useContext } from "react";
import { View, SafeAreaView, Text, StyleSheet, FlatList } from "react-native";
import { useRoute } from "@react-navigation/native";
import axios from "axios";

import { AuthContext } from "../../context/AuthProvider";

import { baseURL } from "../../../env";
import { ADA_USER, ADA_KEY } from "../../../env";

import AsyncStorage from "@react-native-async-storage/async-storage";
import init from "react_native_mqtt";

import { ThemedButton } from "react-native-really-awesome-button";
import { MaterialCommunityIcons } from "react-native-vector-icons";
import { unit, screenMap } from "../../utils/ObjectMap";

import { deviceMode } from "../../utils/ObjectMap";

export default function InteractiveDeviceScreen() {
  const { userToken } = useContext(AuthContext);

  const route = useRoute();
  const [isFirstTime, setIsFisrtTime] = useState(true);
  const [value, setValue] = useState(route.params.curr_value);
  const [currentButton, setCurrentButon] = useState(null);

  const feedType = route.params.device_id.match(/[a-zA-Z-]+/g)[0];
  var clientScreen = null;

  const [clientId, setclientId] = useState("");

  useEffect(() => {
    fetchData();
    connectMQTT();
  }, []);

  useEffect(() => {
    putData();
  }, [value]);

  const fetchData = () => {
    axios
      .get(`${baseURL}/api/v1/device/${route.params.device_id}`, {
        headers: {
          "access-token": userToken,
        },
      })
      .then(function (response) {
        // handle success
        setCurrentButon(
          deviceMode[route.params.type].filter(function (item) {
            return item.value === Number(response.data.data[0].curr_value);
          })[0].key
        );
      })
      .catch(function (error) {
        // handle error
        alert(error.message);
      });
  };

  const connectMQTT = () => {
    function onConnectionLost(responseObject) {
      if (responseObject.errorCode !== 0) {
        console.log("onConnectionLost: " + responseObject.errorMessage);
      }
    }

    function onFailure() {
      console.log("Failed to connect..");
    }

    function onMessageArrived(message) {
      // console.log(
      //   "Interactive device onMessageArrived: " + message.payloadString
      // );
      // setValue(Number(message.payloadString));
      setCurrentButon(
        deviceMode[feedType].filter(function (item) {
          return String(item.value) === message.payloadString;
        })[0].key
      );
    }

    function onConnect() {
      console.log(clientId, " connected successfully...");
      clientScreen.subscribe(
        `thaitran24/feeds/${route.params.home_id}.${route.params.device_id}`
      );
    }

    init({
      size: 10000,
      storageBackend: AsyncStorage,
      defaultExpires: 1000 * 3600 * 24,
      enableCache: true,
      reconnect: true,
      sync: {},
    });

    if (clientScreen === null && clientId == "") {
      setclientId(String(Math.floor(Math.random() * 5000) + 4000));
      clientScreen = new Paho.MQTT.Client("io.adafruit.com", 443, clientId);
      clientScreen.onConnectionLost = onConnectionLost;
      clientScreen.onMessageArrived = onMessageArrived;
      clientScreen.connect({
        onSuccess: onConnect,
        onFailure: onFailure,
        useSSL: true,
        userName: ADA_USER,
        password: ADA_KEY,
      });
    }
  };

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

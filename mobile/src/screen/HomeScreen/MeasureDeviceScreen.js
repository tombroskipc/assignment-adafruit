import React, { useState, useEffect } from "react";
import { View, SafeAreaView, Text, StyleSheet } from "react-native";

import { useRoute } from "@react-navigation/native";

import { ADA_USER, ADA_KEY } from "../../../env";

import AsyncStorage from "@react-native-async-storage/async-storage";
import init from "react_native_mqtt";

import { MaterialCommunityIcons } from "react-native-vector-icons";
import { unit, screenMap } from "../../utils/ObjectMap";

export default function MeasureDeviceScreen() {
  const route = useRoute();
  const [value, setValue] = useState(route.params.curr_value);

  var clientScreen = null;

  const [clientId, setclientId] = useState("");

  useEffect(() => {
    connectMQTT();
  }, []);

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
      // console.log("onMessageArrived: " + message.payloadString);
      setValue(message.payloadString);
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
      setclientId(String(Math.floor(Math.random() * 2000) + 1000));
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

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.info}>
        <View style={styles.data}>
          <Text style={styles.content}>{value}</Text>
          <Text style={styles.unit}>{unit[route.params.type]}</Text>
        </View>
        <View style={styles.icon}>
          <View style={styles.nameContainer}>
            <Text style={styles.name}>{screenMap[route.params.type].name}</Text>
          </View>
          <MaterialCommunityIcons
            name={screenMap[route.params.type].icon}
            color={"#048EF2"}
            size={100}
          />
        </View>
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    flexDirection: "column",
    justifyContent: "center",
    // alignItems: "center",
    // backgroundColor: "#005c99",
  },
  info: {
    justifyContent: "center",
  },
  data: {
    paddingLeft: "10%",
    marginHorizontal: "1%",
    alignItems: "flex-start",
    flexDirection: "row",
  },
  content: {
    fontSize: 120,
    fontFamily: "Arial Rounded MT Bold",
    color: "#048EF2",
  },
  unit: {
    fontSize: 70,
    fontFamily: "Arial Rounded MT Bold",
    color: "#898A8D",
    margin: 10,
  },
  icon: {
    flexDirection: "row",
    justifyContent: "space-between",
    paddingRight: 10,
    paddingLeft: "7%",
  },
  nameContainer: {
    flexDirection: "row",
    alignItems: "center",
    paddingBottom: 30,
  },
  name: {
    fontSize: 45,
    fontFamily: "Arial Rounded MT Bold",
    color: "#898A8D",
  },
});

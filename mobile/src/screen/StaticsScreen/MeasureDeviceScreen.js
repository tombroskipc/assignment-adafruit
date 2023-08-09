import React, { useState, useEffect } from "react";
import { Text, View, SafeAreaView, StyleSheet } from "react-native";
import { useRoute } from "@react-navigation/native";
import { ADA_USER, ADA_KEY } from "../../../env";
import AsyncStorage from "@react-native-async-storage/async-storage";
import init from "react_native_mqtt";
import { LineChart } from "react-native-chart-kit";
import { Dimensions } from "react-native";
import Svg, { Path } from "react-native-svg";

const screenWidth = Dimensions.get("window").width;

export default function MeasureDeviceScreen() {
  const route = useRoute();
  // const [data, setData] = useState([1,2,3,10,20,15,100]);
  const [data, setData] = useState([Number(route.params.curr_value)-2, Number(route.params.curr_value), Number(route.params.curr_value)+2]);
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
      console.log("onMessageArrived: " + message.payloadString);
      setData((prevData) => [...prevData, Number(message.payloadString)]);
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

    if (clientId === "") {
      setclientId(String(Math.floor(Math.random() * 2000) + 1000));
      console.log("clientId:", clientId);
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
  console.log("Check: ", data)

//   const generatePath = (data) => {
//   if (data.length === 0) {
//     return "";
//   }

//   const min = Math.min(...data);
//   const max = Math.max(...data);
//   const range = max - min;
//   const interval = screenWidth / (data.length - 1);
//   return data.reduce(
//     (acc, cur, i) =>
//       i === 0
//         ? `M0,${(1 - (cur - min) / range) * 200}`
//         : `${acc} L${i * interval},${(1 - (cur - min) / range) * 200}`,
//     ""
//   );
// };
  // console.log("Check: ", generatePath(data))

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.graphContainer}>
        {/* <Svg height="200" width={screenWidth}>
          <Path d={generatePath(data)} fill="rgba(4, 142, 242, 0.1)" />
        </Svg> */}
        <LineChart
          
          data={{
            datasets: [
              {
                data: data,
              },
            ],
          }}
          width={screenWidth}
          height={220}
          chartConfig={{
            backgroundColor: "#FFF",
            backgroundGradientFrom: "#FFF",
            backgroundGradientTo: "#FFF",
            decimalPlaces: 2,
            color: (opacity = 1) => `rgba(4, 142, 242, ${opacity})`,
            labelColor: (opacity = 1) => `rgba(137, 138, 141, ${opacity})`,
            style: {
              borderRadius: 16,
            },
            propsForDots: {
              r: "6",
              strokeWidth: "2",
              stroke: "#048EF2",
            },
          }}
          bezier
        />
        
      </View>
      <View>
        <Text>Temp</Text>
      </View>
    </SafeAreaView>
  );
  // path = generatePath(data)
  // console.log(path)
  // return (
  //   <SafeAreaView style={styles.container}>
  //     <View style={styles.graphContainer}>
  //       <Svg height="200" width={screenWidth}>
  //         <Path d={path} />
  //       </Svg>
  //     </View>
  //   </SafeAreaView>
  // );

}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#FFF",
  },
  graphContainer: {
    margin: 10,
  },
});



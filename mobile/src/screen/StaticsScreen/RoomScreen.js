import React, { useEffect, useState, useContext } from "react";
import { useRoute } from "@react-navigation/native";
import axios from "axios";
import { LineChart } from "react-native-chart-kit";
import { Dimensions } from "react-native";
import { screenMap } from "../../utils/ObjectMap";    

import {
  View,
  SafeAreaView,
  FlatList,
  TouchableOpacity,
  Text,
  StyleSheet,
} from "react-native";
import { MaterialCommunityIcons } from "react-native-vector-icons";

import { AuthContext } from "../../context/AuthProvider";
import { baseURL } from "../../../env";


const screenWidth = Dimensions.get("window").width;


export default function RoomScreen({ navigation }) {
  const { userInfo, userToken } = useContext(AuthContext);

  const [roomInfo, setRoomInfo] = useState([]);

  const route = useRoute();

  const [count, setData] = useState(0);
  


  // useEffect(() => {
  //   timer;
  // }, []);

  useEffect(() => {
    fetchDevice();
  }, []);

  const timer = setTimeout(() => {
    setData(count + 1);
    fetchDevice();
  }, 2000);

  const fetchDevice = () => {
    axios
      .get(`${baseURL}/api/v2/device`, {
        headers: {
          "access-token": userToken,
        },
      })
      .then(function (response) {
        // handle success
        console.log(count);
        console.log(Object.values(response.data.data[0].values).slice(1 + count, 10 + count));
        setRoomInfo(
          response.data.data.filter(function (data) {
            let feedId = data._id.match(/[a-zA-Z-]+/g)[0];

            return (
              // data.home_id == userInfo.data.home_id &&
              data.home_id == route.params.home_id &&
              data.room_id == route.params.room_id &&
              data.type !== "movement-sensor"  &&
              screenMap[feedId].type === "Measure"
              // data.type !== "light" &&
              // data.type !== "fan" &&
              // data.type !== "led" &&
              // data.type !== "door"
              
            );
          })
        );
        console.log("Room: Fetch Successful!");
      })
      .catch(function (error) {
        // handle error
        alert(error.message);
      });
  };

  return (
    <SafeAreaView style={styles.container}>
      <FlatList
        data={roomInfo}
        style={styles.list}
        numColumns={1}
        showsVerticalScrollIndicator={false}
        keyExtractor={(item) => item._id}
        renderItem={({ item }) => (
          // <TouchableOpacity
          //   style={styles.card}
          //   onPress={() => {
          //     // clearTimeout(timer);
          //     // console.log("Device_id:", item._id);
          //     navigation.navigate(`${screenMap[item.type].type}Device`, {
          //       home_id: route.params.home_id,
          //       device_id: item._id,
          //       curr_value: item.curr_value,
          //       type: item.type,
          //     });
          //   }}
          // >
          //   <MaterialCommunityIcons
          //     name={screenMap[item.type].icon}
          //     color={"#048EF2"}
          //     size={75}
          //   />
          //   <View>
          //     <Text>{screenMap[item.type].name}</Text>
          //   </View>
          // </TouchableOpacity>
          <View>
          <LineChart
          
          data={{
            datasets: [
              {
                data: Object.values(item.values).slice(1 + count, 10 + count),
              },
            ],
          }}
          width={screenWidth}
          height={190}
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
              r: "3",
              strokeWidth: "1",
              stroke: "#048EF2",
            },
          }}
          bezier
          
        />
        
      <View style={styles.legend}>
        <Text>{item.name}</Text>
      </View>
       </View>

        )}
      />
    </SafeAreaView>
  );
  // return (
  //   <SafeAreaView style={styles.container}>
  //     <View style={styles.graphContainer}>
  //       {/* <Svg height="200" width={screenWidth}>
  //         <Path d={generatePath(data)} fill="rgba(4, 142, 242, 0.1)" />
  //       </Svg> */}
  //       <LineChart
          
  //         data={{
  //           datasets: [
  //             {
  //               data: data,
  //             },
  //           ],
  //         }}
  //         width={screenWidth}
  //         height={220}
  //         chartConfig={{
  //           backgroundColor: "#FFF",
  //           backgroundGradientFrom: "#FFF",
  //           backgroundGradientTo: "#FFF",
  //           decimalPlaces: 2,
  //           color: (opacity = 1) => `rgba(4, 142, 242, ${opacity})`,
  //           labelColor: (opacity = 1) => `rgba(137, 138, 141, ${opacity})`,
  //           style: {
  //             borderRadius: 16,
  //           },
  //           propsForDots: {
  //             r: "6",
  //             strokeWidth: "2",
  //             stroke: "#048EF2",
  //           },
  //         }}
  //         bezier
  //       />
        
  //     </View>
  //     <View>
  //       <Text>Temp</Text>
  //     </View>
  //   </SafeAreaView>
  // );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    width: "100%",
    backgroundColor: "#F2F2F2",
    alignItems: "center",
    marginVertical: 0,
  },
  list: {
    // width: "100%",
    alignContent: "center",
  },
  card: {
    paddingHorizontal: 8,
    paddingVertical: 6,
    borderRadius: 20,
    height: 175,
    width: 175,
    padding: 10,
    marginHorizontal: "1%",
    marginBottom: 10,
    textAlign: "center",
    alignItems: "center",
    backgroundColor: "#FFFFFF",
    justifyContent: "center",
  },
  legend: {
    alignItems: "center",
    alignContent: "center",
    backgroundColor: "#ffffff"
  }
});

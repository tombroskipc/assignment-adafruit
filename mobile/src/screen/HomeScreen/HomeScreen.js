import React, { useContext, useEffect, useState } from "react";
import {
  Text,
  View,
  SafeAreaView,
  StyleSheet,
  FlatList,
  TouchableOpacity,
  DeviceEventEmitter,
} from "react-native";
import { MaterialCommunityIcons } from "react-native-vector-icons";

import { useRoute } from "@react-navigation/native";
import axios from "axios";

import { AuthContext } from "../../context/AuthProvider";
import { baseURL } from "../../../env";

export default function HomeScreen({ navigation }) {
  const { userInfo, userToken } = useContext(AuthContext);

  const [room, setRoom] = useState([]);

  const route = useRoute();

  // useEffect(() => {
  //   timer;
  // }, []);

  useEffect(() => {
    fetchRoom();
  }, []);

  // const timer = setTimeout(() => {
  //   fetchRoom();
  // }, 1500);

  const fetchRoom = () => {
    axios
      .get(`${baseURL}/api/v1/room`, {
        headers: {
          "access-token": userToken,
        },
      })
      .then(function (response) {
        // handle success

        setRoom(
          response.data.data.filter(function (item) {
            // return item.home_id == userInfo.data.home_id;
            return (item.home_id = route.params.home_id);
          })
        );
        console.log("Home: fetch Successful!");
      })
      .catch(function (error) {
        // handle error
        alert(error.message);
      });
  };

  return (
    <SafeAreaView style={styles.container}>
      <FlatList
        data={room}
        style={styles.list}
        numColumns={2}
        showsVerticalScrollIndicator={false}
        keyExtractor={(item) => item._id}
        renderItem={({ item }) => (
          <TouchableOpacity
            style={styles.card}
            onPress={() => {
              // clearTimeout(timer);
              navigation.navigate("Room", {
                home_id: item.home_id,
                room_id: item._id,
                name: item.name,
              });
            }}
          >
            <MaterialCommunityIcons
              name="bed-double-outline"
              color={"#048EF2"}
              size={90}
            />
            <View>
              <Text>{item.name}</Text>
            </View>
          </TouchableOpacity>
        )}
      />
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    width: "100%",
    backgroundColor: "#F2F2F2",
    alignItems: "flex-start",
    marginVertical: 0,
    marginHorizontal: "5%",
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
});

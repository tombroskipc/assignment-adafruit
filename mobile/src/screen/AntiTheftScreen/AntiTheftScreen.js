import React, { useState, useContext } from "react";
import { View, Text, StyleSheet, SafeAreaView } from "react-native";

import { Video } from "expo-av";

import { AuthContext } from "../../context/AuthProvider";
import LightVideo from "/home/xuan/BKU/Third Year - 22/Second Term/Project/mobile/YoloHome/mobile/assets/345494089_6146328358794501_1755358773750852284_n.mp4";

export default function AntiTheftScreen() {
  const { decodedVideo, detectingTime, setDetectingTime } =
    useContext(AuthContext);

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.time}>
        <Text style={styles.timeText}>
          Latest time:{" "}
          {detectingTime === null
            ? "No update"
            : detectingTime.toLocaleString()}
        </Text>
      </View>
      <View style={styles.videoContainer}>
        {detectingTime !== null ? (
          <Video
            source={LightVideo}
            style={styles.video}
            useNativeControls
            resizeMode="cover"
            isLooping
          />
        ) : (
          <View style={styles.nullVideo}>
            <Text style={styles.nullText}>No Available Video</Text>
          </View>
        )}
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: "center",
  },
  time: {
    flex: 0.25,
    flexDirection: "row",
    alignItems: "flex-end",
    // backgroundColor: "#cccccc",
    margin: 10,
  },
  timeText: {
    fontFamily: "Arial Rounded MT Bold",
    fontSize: 20,
  },
  videoContainer: {
    flex: 0.75,
    // width: "100%",
    // backgroundColor: "#cccccc",
    alignItems: "center",
  },
  video: {
    top: 0,
    left: 0,
    bottom: 0,
    right: 0,
    height: 250,
    width: "100%",
  },
  nullVideo: {
    height: 250,
    marginTop: "10%",
  },
  nullText: {
    fontFamily: "Arial Rounded MT Bold",
    fontSize: 30,
    color: "#cccccc",
  },
});

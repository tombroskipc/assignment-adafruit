export const screenMap = {
  fan: {
    type: "Interactive",
    icon: "fan",
    name: "Fan",
  },
  door: {
    type: "Interactive",
    icon: "door",
    name: "Door",
  },
  led: {
    type: "Interactive",
    icon: "lightbulb-multiple-outline",
    name: "Led",
  },
  "temp-sensor": {
    type: "Measure",
    icon: "thermometer-low",
    name: "Temperature",
    min: 15,
    max: 35,
  },
  "light-sensor": {
    type: "Measure",
    icon: "alarm-light-outline",
    name: "Light strength",
  },
  "humid-sensor": {
    type: "Measure",
    icon: "water-percent",
    name: "Humidity",
    min: 30,
    max: 80,
  },
  "movement-sensor": {
    type: "Measure",
    icon: "run-fast",
    name: "Movement",
  },
};

export const deviceMode = {
  fan: [
    { key: "Off", value: 0, color: "#8c8c8c", icon: "fan-remove" },
    { key: "25%", value: 25, color: "#33adff", icon: "fan-speed-1" },
    { key: "50%", value: 50, color: "#b3b300", icon: "fan-speed-2" },
    { key: "75%", value: 75, color: "#ff9900", icon: "fan-speed-3" },
    { key: "100%", value: 100, color: "#6b117a", icon: "fan-plus" },
  ],
  led: [
    { key: "Off", value: 0, color: "#8c8c8c", icon: "lightbulb-outline" },
    { key: "Red", value: 1, color: "#cc3300", icon: "lightbulb-on-outline" },
    { key: "Yellow", value: 2, color: "#b3b300", icon: "lightbulb-on-outline" },
    { key: "Blue", value: 3, color: "#0099ff", icon: "lightbulb-on-outline" },
  ],
  door: [
    { key: "Closed", value: 0, color: "#8c8c8c", icon: "lock" },
    { key: "Opened", value: 1, color: "#669900", icon: "lock-open-variant" },
  ],
};

export const unit = {
  "temp-sensor": "\u00b0C",
  "light-sensor": "%",
  "humid-sensor": "%",
};

import React from "react";
import Navigation from "./Navigation";

import { AuthProvider } from "../context/AuthProvider";

export default function Provider() {
  return (
    <AuthProvider>
      <Navigation />
    </AuthProvider>
  );
}

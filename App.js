import React from "react";
import { SafeAreaView } from "react-native";
import LoginScreen from "./src/LoginScreen";
import SignUpScreen from "./src/Signup";
import { createStackNavigator } from "@react-navigation/stack";
import { NavigationContainer } from "@react-navigation/native";
import Home from "./src/Home";
import ProfileScreen from "./src/ProfileScreen";
import RecieveScreen from "./src/Recieve";
import Buy from "./src/Buy";
import Send from "./src/Send";
import Dvd from "./src/dvd";

const Stack = createStackNavigator();
const App = () => {
  return (
    <SafeAreaView style={{ flex: 1 }}>
      <NavigationContainer>
        <Stack.Navigator>
          <Stack.Screen
            options={{ headerShown: false }}
            name="Login"
            component={LoginScreen}
          />
          <Stack.Screen
            options={{ headerShown: false }}
            name="Signup"
            component={SignUpScreen}
          />          
          <Stack.Screen
            options={{ headerShown: false }}
            name="dvd"
            component={Dvd}
          />
          <Stack.Screen
            options={{ headerShown: false }}
            name="Home"
            component={Home}
          />
          <Stack.Screen
            options={{ headerShown: true }}
            name="Profile"
            component={ProfileScreen}
          />
          <Stack.Screen
            options={{ headerShown: true }}
            name="Recieve"
            component={RecieveScreen}
          />
          <Stack.Screen
            options={{ headerShown: true }}
            name="Send"
            component={Send}
          />
          <Stack.Screen
            options={{ headerShown: true }}
            name="Buy"
            component={Buy}
          />
        </Stack.Navigator>
      </NavigationContainer>
      {/* <LoginScreen /> */}
    </SafeAreaView>
  );
};

export default App;

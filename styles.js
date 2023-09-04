import { StyleSheet } from "react-native";

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
    backgroundColor: "whitesmoke",// Set the background color to full blue
  },
  heading: {
    fontSize: 32,
    fontWeight: "bold",
    marginBottom: 32,
    color: "skyblue", // Set the heading color to white
  },
  input: {
    width: "85%",
    padding: 15,
    color: "black",
    borderWidth: 1,
    borderColor: "skyblue",
    borderRadius: 12, // Set border radius to make it round
    marginBottom: 16,
    backgroundColor: "whitesmoke", // Set the input background color to white
  },
  button: {
    backgroundColor: "skyblue",
    width: 120,
    marginTop: 30,
    padding: 13,
    borderRadius: 12, // Set border radius to make it round
  },
  signup: {
    backgroundColor: "skyblue",
    width: 120,
    marginTop: 15,
    borderRadius: 12, // Set border radius to make it round
  },
  buttonText: {
    color: "black",
    fontSize: 16,
    fontWeight: "bold",
    textAlign: "center",
  },
});

export default styles;


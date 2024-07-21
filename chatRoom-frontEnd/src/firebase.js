// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getFirestore } from 'firebase/firestore';
import { getAuth, createUserWithEmailAndPassword, signInWithEmailAndPassword } from "firebase/auth";
import { signOut as FBsignOut } from "firebase/auth";
import { onAuthStateChanged as onFBAuthStateChanged } from "firebase/auth";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyDI1ztXQSvWGUqD9siSMCCO4tW5lJhR-R0",
  authDomain: "fir-withvite.firebaseapp.com",
  projectId: "fir-withvite",
  storageBucket: "fir-withvite.appspot.com",
  messagingSenderId: "197627185211",
  appId: "1:197627185211:web:8053b7bddc71e36629341e"
};


// Initialize Firebase
const app = initializeApp(firebaseConfig);

export const db = getFirestore(app);
export const auth = getAuth();

export function signUp(email, password) {
    return createUserWithEmailAndPassword(auth, email, password)
}

export function signIn(email, password) {
    return signInWithEmailAndPassword(auth, email, password);
}

export function signOut() {
    return FBsignOut(auth);
}

export function onAuthStateChanged(fn) {
    return onFBAuthStateChanged(auth, fn);
}
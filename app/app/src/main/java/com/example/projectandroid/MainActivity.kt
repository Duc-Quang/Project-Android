package com.example.projectandroid
//https://developer.android.com/guide/topics/ui/ui-events#kotlin
import android.annotation.SuppressLint
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import com.google.android.material.button.MaterialButton

class MainActivity : AppCompatActivity() {
    @SuppressLint("WrongViewCast")
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.welcome)
        val btnSignIn = findViewById<MaterialButton>(R.id.signin)
        btnSignIn.setOnClickListener {
            setContentView(R.layout.signin)
        }
        val btnSignUp = findViewById<MaterialButton>(R.id.signup)
        btnSignUp.setOnClickListener {
            setContentView(R.layout.signup)
        }
//        val btnSignUpHere = findViewById<MaterialButton>(R.id.signUpHere)
//        btnSignUpHere.setOnClickListener {
//            setContentView(R.layout.signup)
//        }
//        val btnBack = findViewById<MaterialButton>(R.id.buttonBack)
//        btnBack.setOnClickListener {
//            setContentView(R.layout.welcome)
//        }
//        val backBtn = findViewById<MaterialButton>(R.id.backButton)
//        backBtn.setOnClickListener {
//            setContentView(R.layout.welcome)
//        }
    }
}
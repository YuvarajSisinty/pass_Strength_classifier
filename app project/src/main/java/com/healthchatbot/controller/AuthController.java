package com.healthchatbot.controller;

import com.healthchatbot.dto.AuthRequest;
import com.healthchatbot.dto.AuthResponse;
import com.healthchatbot.service.AuthService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/auth")
@CrossOrigin(origins = "*")
public class AuthController {

    @Autowired
    private AuthService authService;

    @PostMapping("/signup")
    public ResponseEntity<?> signup(@RequestBody AuthRequest request) {
        try {
            authService.signup(request.getUsername(), request.getEmail(), request.getPassword());
            String token = authService.login(request.getUsername(), request.getPassword());
            
            AuthResponse response = new AuthResponse(token, request.getUsername(), "Signup successful");
            return ResponseEntity.ok(response);
        } catch (RuntimeException e) {
            return ResponseEntity.status(HttpStatus.BAD_REQUEST)
                    .body(new AuthResponse(null, null, e.getMessage()));
        }
    }

    @PostMapping("/login")
    public ResponseEntity<?> login(@RequestBody AuthRequest request) {
        try {
            String token = authService.login(request.getUsername(), request.getPassword());
            AuthResponse response = new AuthResponse(token, request.getUsername(), "Login successful");
            return ResponseEntity.ok(response);
        } catch (RuntimeException e) {
            return ResponseEntity.status(HttpStatus.UNAUTHORIZED)
                    .body(new AuthResponse(null, null, e.getMessage()));
        }
    }
}


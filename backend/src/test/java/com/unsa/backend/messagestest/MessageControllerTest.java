package com.unsa.backend.messagestest;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.doThrow;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.never;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;
import static org.hamcrest.Matchers.is;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;
import static org.springframework.security.test.web.servlet.request.SecurityMockMvcRequestPostProcessors.*;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import com.fasterxml.jackson.databind.ObjectMapper;

import java.util.ArrayList;
import java.util.List;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.MediaType;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.test.web.servlet.MockMvc;

import com.unsa.backend.messages.MessageController;
import com.unsa.backend.messages.MessageModel;
import com.unsa.backend.messages.MessageService;
import com.unsa.backend.users.Role;

@SpringBootTest
@AutoConfigureMockMvc
@DisplayName("Message Controller Test")
@ExtendWith(MockitoExtension.class)
class MessageControllerTest {

    private static final String URL_BASE = "/message";

    @MockBean
    private MessageService messageService;

    private MockMvc mockMvc;

    @Autowired
    void setMockMvc(MockMvc mockMvc) {
        this.mockMvc = mockMvc;
    }

    @Test
    @DisplayName("Create Message - Invalid Message")
    void createMessageInvalidMessage() throws Exception {
        // Arrange
        MessageModel invalidMessage = new MessageModel(); // Mensaje sin datos válidos

        // Act & Assert
        mockMvc.perform(post("/message") // Asegúrate de que la ruta coincida con la configuración del controlador
                .contentType(MediaType.APPLICATION_JSON)
                .content(asJsonString(invalidMessage)))
                .andExpect(status().isBadRequest());

        verify(messageService, never()).createMessage(any());
    }

    @Test
    @DisplayName("Get Messages - Success")
    void getMessagesSuccess() throws Exception {
        Long chatId = 1L;
        List<MessageModel> messages = new ArrayList<>();
        when(messageService.getMessages(chatId)).thenReturn(messages);

        mockMvc.perform(get(URL_BASE + "/{chatId}", chatId))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$").isArray());

        verify(messageService).getMessages(chatId);
    }

    // Utilidad para convertir un objeto a JSON
    private static String asJsonString(final Object obj) {
        try {
            return new ObjectMapper().writeValueAsString(obj);
        } catch (Exception e) {
            throw new RuntimeException(e);
        }
    }
}

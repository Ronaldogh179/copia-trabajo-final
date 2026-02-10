"""
Módulo de voz SEGURO - Funciona con o sin micrófono
Optimizado para Visual Studio Code
"""

import threading
import time


class VoiceAssistant:
    def __init__(self):
        self.voice_available = True  # Siempre disponible
        self.is_listening = False
        self.tts_engine = None
        self.use_real_microphone = False

        print("🎤 Inicializando sistema de voz...")

        # 1. Cargar síntesis de voz (pyttsx3)
        try:
            import pyttsx3

            self.tts_engine = pyttsx3.init()

            # Configurar voz
            voices = self.tts_engine.getProperty("voices")
            for voice in voices:
                if "spanish" in voice.name.lower():
                    self.tts_engine.setProperty("voice", voice.id)
                    break

            self.tts_engine.setProperty("rate", 150)
            self.tts_engine.setProperty("volume", 0.8)
            print("  ✅ Síntesis de voz: ACTIVA")
        except Exception as e:
            print(f"  ⚠️  Síntesis de voz: {str(e)[:50]}")
            self.tts_engine = None

        # 2. Verificar reconocimiento de voz
        try:
            import speech_recognition as sr

            self.recognizer = sr.Recognizer()
            print("  ✅ SpeechRecognition: CARGADO")

            # NOTA: No intentamos crear Microphone() aquí
            # para evitar errores en Python 3.14
            self.use_real_microphone = False  # Por defecto simulado

        except ImportError:
            print("  ❌ SpeechRecognition no instalado")
            self.use_real_microphone = False
        except Exception as e:
            print(f"  ⚠️  Error reconocimiento: {str(e)[:50]}")
            self.use_real_microphone = False

        print("✅ Sistema de voz listo (modo simulado)")

    def hablar(self, texto):
        """Texto a voz - Siempre funciona"""
        print(f"🤖 Asistente: {texto}")

        if self.tts_engine:
            try:

                def _hablar():
                    self.tts_engine.say(texto)
                    self.tts_engine.runAndWait()

                thread = threading.Thread(target=_hablar, daemon=True)
                thread.start()
            except:
                pass  # Silenciar errores

    def escuchar(self, timeout=5):
        """Escuchar comando - Modo simulado para VS Code"""
        print("\n🎤 [MODO VOZ SIMULADO]")
        print("=" * 40)
        print("Comandos disponibles:")
        print("1. crear tarea 'Reunión importante'")
        print("2. listar tareas")
        print("3. tareas pendientes")
        print("4. ayuda")
        print("5. salir")
        print("=" * 40)
        print("Escribe el número o comando y presiona Enter:")

        try:
            # Leer entrada del usuario en VS Code
            import sys

            # Usamos input() normal para VS Code
            comando = input("> ").strip()

            # Mapear números a comandos
            comandos_map = {
                "1": "crear tarea reunión importante",
                "2": "listar tareas",
                "3": "tareas pendientes",
                "4": "ayuda",
                "5": "salir",
            }

            if comando in comandos_map:
                comando = comandos_map[comando]

            print(f"✅ Comando recibido: {comando}")
            return comando.lower()

        except Exception as e:
            print(f"⚠️  Error lectura: {e}")
            return None

    def iniciar_modo_voz(self):
        """Iniciar modo voz interactivo"""
        self.is_listening = True
        self.hablar("Modo voz activado. Usa la terminal para ingresar comandos.")

        print("\n" + "=" * 50)
        print("🔊 MODO VOZ ACTIVADO")
        print("=" * 50)
        print("Instrucciones:")
        print("1. Los comandos se ingresan por TECLADO")
        print("2. La respuesta se escuchará por ALTAVOCES")
        print("3. Escribe 'ayuda' para ver comandos")
        print("4. Escribe 'salir' para terminar")
        print("=" * 50)

        return True

    def detener_modo_voz(self):
        """Detener modo voz"""
        self.is_listening = False
        self.hablar("Modo voz desactivado.")
        print("\n🔊 Modo voz desactivado")


# Instancia global SEGURA
try:
    voice_assistant = VoiceAssistant()
except Exception as e:
    print(f"❌ Error crítico en voz: {e}")

    # Dummy de emergencia
    class EmergencyVoice:
        def __init__(self):
            self.voice_available = True
            self.is_listening = False

        def hablar(self, texto):
            print(f"🤖: {texto}")

        def escuchar(self, timeout=5):
            return None

        def iniciar_modo_voz(self):
            print("🔊 Modo voz no disponible")
            return False

        def detener_modo_voz(self):
            pass

    voice_assistant = EmergencyVoice()

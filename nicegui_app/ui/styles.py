class Style:
    # --- Kontenery i Karty ---
    # Podstawowa karta (używana w Chatterbox, Single Gen)
    CARD = "w-full p-4 border border-gray-200 rounded-xl gap-6 bg-white"
    # Karta z cieniem (używana w Audiobook)
    CARD_SHADOW = (
        "w-full p-4 border border-gray-200 rounded-xl shadow-md bg-white items-center"
    )
    # Karta bez cienia (wewnątrz tabów)
    CARD_FLAT = "w-full h-[460px] p-4 border border-gray-200 rounded-xl shadow-none"

    # --- Typografia ---
    # Nagłówki sekcji (np. "Text to synthesize")
    HEADING_H3 = "font-semibold text-gray-700 w-full text-center"
    # Etykiety przy inputach
    LABEL = "font-semibold text-gray-700"
    # Subtelne napisy (np. w headerze)
    # SUBTITLE = 'text-lg text-gray-300 font-light'

    # --- Elementy Formularzy (Inputy) ---
    # Standardowy input/select (dodaj .props('outlined dense') w kodzie komponentu)
    INPUT = "w-full"
    # Input/Textarea o konkretnej wysokości
    TEXTAREA_L = "w-full h-24"
    TEXTAREA_XL = "w-full h-full"

    # --- Przyciski (Buttons) ---
    # Główny przycisk akcji (zastępuje props color=indigo)
    # BTN_PRIMARY = 'w-full font-bold rounded-lg shadow-md bg-indigo-500 text-white hover:bg-indigo-600 transition-colors'
    # Wersja o konkretnej wysokości (często używana u Ciebie)
    BTN_PRIMARY_H12 = BTN_PRIMARY + " h-12 text-base"
    # Mały przycisk (np. "Detect Speakers")
    BTN_PRIMARY = "w-full h-10 font-bold text-sm rounded-lg shadow-md bg-indigo-500 text-white hover:bg-indigo-600"

    # Przycisk "Danger" / Usuwanie
    BTN_DANGER = "bg-red-500 text-white hover:bg-red-600"
    # Ikony akcji (Play/Regenerate w liście)
    BTN_ICON_ACTION = "text-indigo-600 bg-transparent hover:bg-indigo-50"

    # --- Specyficzne komponenty ---
    # Sekcja Upload w Chatterbox
    UPLOAD_BOX = "w-full h-full border-2 border-dashed border-slate-300 rounded-lg items-center justify-center bg-slate-50 transition-colors group-hover:bg-slate-100 group-hover:border-slate-400 gap-1"
    # Kontener na suwak (Slider)
    SLIDER_BOX = "w-full mt-2 p-2 bg-gray-50 rounded-lg border border-gray-100"
    # Obszar scrollowania
    SCROLL_BOX = "w-full h-52 border border-gray-200 rounded-md p-2"

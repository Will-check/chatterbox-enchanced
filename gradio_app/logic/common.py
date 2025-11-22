import gradio as gr
import os
from gradio_app.models.tts_model import get_or_load_model, set_seed


LANGUAGE_CONFIG = {
    "ar": {
        "audio": "./samples/ar_prompts2.flac",
        "text": "في الشهر الماضي، وصلنا إلى معلم جديد بمليارين من المشاهدات على قناتنا على يوتيوب."
    },
    "da": {
        "audio": "./samples/da_m1.flac",
        "text": "Sidste måned nåede vi en ny milepæl med to milliarder visninger på vores YouTube-kanal."
    },
    "de": {
        "audio": "./samples/de_f1.flac",
        "text": "Letzten Monat haben wir einen neuen Meilenstein erreicht: zwei Milliarden Aufrufe auf unserem YouTube-Kanal."
    },
    "el": {
        "audio": "./samples/el_m.flac",
        "text": "Τον περασμένο μήνα, φτάσαμε σε ένα νέο ορόσημο με δύο δισεκατομμύρια προβολές στο κανάλι μας στο YouTube."
    },
    "en": {
        "audio": "./samples/en_f1.flac",
        "text": "Last month, we reached a new milestone with two billion views on our YouTube channel."
    },
    "es": {
        "audio": "./samples/es_f1.flac",
        "text": "El mes pasado alcanzamos un nuevo hito: dos mil millones de visualizaciones en nuestro canal de YouTube."
    },
    "fi": {
        "audio": "./samples/fi_m.flac",
        "text": "Viime kuussa saavutimme uuden virstanpylvään kahden miljardin katselukerran kanssa YouTube-kanavallamme."
    },
    "fr": {
        "audio": "./samples/fr_f1.flac",
        "text": "Le mois dernier, nous avons atteint un nouveau jalon avec deux milliards de vues sur notre chaîne YouTube."
    },
    "he": {
        "audio": "./samples/he_m1.flac",
        "text": "בחודש שעבר הגענו לאבן דרך חדשה עם שני מיליארד צפיות בערוץ היוטיוב שלנו."
    },
    "hi": {
        "audio": "./samples/hi_f1.flac",
        "text": "पिछले महीने हमने एक नया मील का पत्थर छुआ: हमारे YouTube चैनल पर दो अरब व्यूज़।"
    },
    "it": {
        "audio": "./samples/it_m1.flac",
        "text": "Il mese scorso abbiamo raggiunto un nuovo traguardo: due miliardi di visualizzazioni sul nostro canale YouTube."
    },
    "ja": {
        "audio": "./samples/ja_prompts1.flac",
        "text": "先月、私たちのYouTubeチャンネルで二十億回の再生回数という新たなマイルストーンに到達しました。"
    },
    "ko": {
        "audio": "./samples/ko_f.flac",
        "text": "지난달 우리는 유튜브 채널에서 이십억 조회수라는 새로운 이정표에 도달했습니다."
    },
    "ms": {
        "audio": "./samples/ms_f.flac",
        "text": "Bulan lepas, kami mencapai pencapaian baru dengan dua bilion tontonan di saluran YouTube kami."
    },
    "nl": {
        "audio": "./samples/nl_m.flac",
        "text": "Vorige maand bereikten we een nieuwe mijlpaal met twee miljard weergaven op ons YouTube-kanaal."
    },
    "no": {
        "audio": "./samples/no_f1.flac",
        "text": "Forrige måned nådde vi en ny milepæl med to milliarder visninger på YouTube-kanalen vår."
    },
    "pl": {
        "audio": "./samples/pl_m.flac",
        "text": "W zeszłym miesiącu osiągnęliśmy nowy kamień milowy z dwoma miliardami wyświetleń na naszym kanale YouTube."
    },
    "pt": {
        "audio": "./samples/pt_m1.flac",
        "text": "No mês passado, alcançámos um novo marco: dois mil milhões de visualizações no nosso canal do YouTube."
    },
    "ru": {
        "audio": "./samples/ru_m.flac",
        "text": "В прошлом месяце мы достигли нового рубежа: два миллиарда просмотров на нашем YouTube-канале."
    },
    "sv": {
        "audio": "./samples/sv_f.flac",
        "text": "Förra månaden nådde vi en ny milstolpe med två miljarder visningar på vår YouTube-kanal."
    },
    "sw": {
        "audio": "./samples/sw_m.flac",
        "text": "Mwezi uliopita, tulifika hatua mpya ya maoni ya bilioni mbili kweny kituo chetu cha YouTube."
    },
    "tr": {
        "audio": "./samples/tr_m.flac",
        "text": "Geçen ay YouTube kanalımızda iki milyar görüntüleme ile yeni bir dönüm noktasına ulaştık."
    },
    "zh": {
        "audio": "./samples/zh_f2.flac",
        "text": "上个月，我们达到了一个新的里程碑. 我们的YouTube频道观看次数达到了二十亿次，这绝对令人难以置信。"
    },
}

INITIAL_LANG = "en"
DEFAULT_VOICE_LIBRARY = "./voice_library"
CONFIG_FILE = "audiobook_config.json"

DEFAULT_AUDIO_PATHS = [
    os.path.normpath(v["audio"])
    for v in LANGUAGE_CONFIG.values()
    if v.get("audio")
]

def is_default_audio_path(path: str | None) -> bool:
    if not path:
        return True

    p_norm = os.path.normpath(path)
    p_base = os.path.basename(p_norm)

    for a in DEFAULT_AUDIO_PATHS:
        a_norm = os.path.normpath(a)
        a_base = os.path.basename(a_norm)

        if p_norm == a_norm:
            return True
        if p_norm.endswith(a_norm):
            return True
        if p_base == a_base:
            return True

    return False

def default_audio_for_ui(lang: str) -> str | None:
    return LANGUAGE_CONFIG.get(lang, {}).get("audio")

def default_text_for_ui(lang: str) -> str:
    return LANGUAGE_CONFIG.get(lang, {}).get("text", "")

def on_language_change(lang, current_ref, current_text):
    new_text = default_text_for_ui(lang)

    if is_default_audio_path(current_ref):
        return default_audio_for_ui(lang), new_text

    return gr.update(value=current_ref), new_text

def generate_tts_audio(
    text_input: str,
    language_id: str,
    audio_prompt_path_input: str = None,
    exaggeration_input: float = 0.5,
    temperature_input: float = 0.8,
    seed_num_input: int = 0,
    cfgw_input: float = 0.5
):
    """
    Generate high-quality speech audio from text using Chatterbox Multilingual model with optional reference audio styling.
    Supported languages: English, French, German, Spanish, Italian, Portuguese, and Hindi.
    
    This tool synthesizes natural-sounding speech from input text. When a reference audio file 
    is provided, it captures the speaker's voice characteristics and speaking style. The generated audio 
    maintains the prosody, tone, and vocal qualities of the reference speaker, or uses default voice if no reference is provided.

    Args:
        text_input (str): The text to synthesize into speech (maximum 300 characters)
        language_id (str): The language code for synthesis (eg. en, fr, de, es, it, pt, hi)
        audio_prompt_path_input (str, optional): File path or URL to the reference audio file that defines the target voice style. Defaults to None.
        exaggeration_input (float, optional): Controls speech expressiveness (0.25-2.0, neutral=0.5, extreme values may be unstable). Defaults to 0.5.
        temperature_input (float, optional): Controls randomness in generation (0.05-5.0, higher=more varied). Defaults to 0.8.
        seed_num_input (int, optional): Random seed for reproducible results (0 for random generation). Defaults to 0.
        cfgw_input (float, optional): CFG/Pace weight controlling generation guidance (0.2-1.0). Defaults to 0.5, 0 for language transfer. 

    Returns:
        tuple[int, np.ndarray]: A tuple containing the sample rate (int) and the generated audio waveform (numpy.ndarray)
    """
    current_model = get_or_load_model()

    if current_model is None:
        raise RuntimeError("TTS model is not loaded.")

    if seed_num_input != 0:
        set_seed(int(seed_num_input))

    print(f"Generating audio for text: '{text_input[:50]}...'")
    
    # Handle optional audio prompt
    chosen_prompt = audio_prompt_path_input or default_audio_for_ui(language_id)

    generate_kwargs = {
        "exaggeration": exaggeration_input,
        "temperature": temperature_input,
        "cfg_weight": cfgw_input,
    }
    if chosen_prompt:
        generate_kwargs["audio_prompt_path"] = chosen_prompt
        print(f"Using audio prompt: {chosen_prompt}")
    else:
        print("No audio prompt provided; using default voice.")
        
    wav = current_model.generate(
        text_input[:300],  # Truncate text to max chars
        language_id=language_id,
        **generate_kwargs
    )
    print("Audio generation complete.")
    return (current_model.sr, wav.squeeze(0).numpy())
TAG_DEFINITIONS = {
    "all": {"bg": "#e3f2fd", "border": "#1e88e5", "text": "#0d47a1"},
    "medical": {"bg": "#fff3e0", "border": "#fb8c00", "text": "#e65100"},
    "business": {"bg": "#fce4ec", "border": "#d81b60", "text": "#880e4f"},
    "motorsport": {"bg": "#e0f7fa", "border": "#00acc1", "text": "#006064"},
    "f1": {"bg": "#f1f8e9", "border": "#7cb342", "text": "#33691e"},
    "golf": {"bg": "#f1f8e9", "border": "#7cb342", "text": "#33691e"},
}

FALLBACK_PALETTES = [
    {"bg": "#e3f2fd", "border": "#1e88e5", "text": "#0d47a1"},  # 1: Blue
    {"bg": "#ede7f6", "border": "#5e35b1", "text": "#4a148c"},  # 2: Purple
    {"bg": "#e8f5e9", "border": "#43a047", "text": "#1b5e20"},  # 3: Green
    {"bg": "#fff3e0", "border": "#fb8c00", "text": "#e65100"},  # 4: Orange
    {"bg": "#fce4ec", "border": "#d81b60", "text": "#880e4f"},  # 5: Pink
    {"bg": "#f3e5f5", "border": "#8e24aa", "text": "#4a148c"},  # 6: Deep Purple
    {"bg": "#e0f7fa", "border": "#00acc1", "text": "#006064"},  # 7: Cyan
    {"bg": "#e0f2f1", "border": "#00897b", "text": "#004d40"},  # 8: Teal
    {"bg": "#e8eaf6", "border": "#3949ab", "text": "#1a237e"},  # 9: Indigo
    {"bg": "#efebe9", "border": "#6d4c41", "text": "#3e2723"},  # 10: Brown
    {"bg": "#f1f8e9", "border": "#7cb342", "text": "#33691e"},  # 11: Light Green
    {"bg": "#fffde7", "border": "#fdd835", "text": "#f57f17"},  # 12: Yellow
    {"bg": "#fff8e1", "border": "#ffb300", "text": "#ff6f00"},  # 13: Amber
    {"bg": "#ffe0b2", "border": "#f57c00", "text": "#e65100"},  # 14: Dark Orange
    {"bg": "#f5f5f5", "border": "#757575", "text": "#212121"},  # 15: Grey
    {"bg": "#eceff1", "border": "#546e7a", "text": "#263238"},  # 16: Blue Grey
    {"bg": "#ffebee", "border": "#e53935", "text": "#b71c1c"},  # 17: Red
    {"bg": "#f9fbe7", "border": "#c0ca33", "text": "#827717"},  # 18: Lime
    {"bg": "#f0f4c3", "border": "#afb42b", "text": "#558b2f"},  # 19: Olive-Lime
    {"bg": "#e1f5fe", "border": "#039be5", "text": "#01579b"},  # 20: Light Blue
    {"bg": "#e0e0e0", "border": "#616161", "text": "#212121"},  # 21: Charcoal Grey
    {"bg": "#fce4ec", "border": "#ec407a", "text": "#ad1457"},  # 22: Magenta Rose
]

MOCK_EVENTS = [
    {
        "title": "All Day Event",
        "start": "2026-06-01",
        "classNames": ["all", "medical", "personal"],
        "link": "https://www.marcelldls.lol/0",
    },
    {
        "title": "Long Event",
        "start": "2026-06-07",
        "end": "2026-06-10",
        "classNames": ["all", "test"],
        "link": "https://www.marcelldls.lol/0",
    },
    {
        "title": "Repeating Event",
        "start": "2026-06-09T16:00:00",
        "classNames": ["all"],
        "link": "https://www.marcelldls.lol/0",
    },
    {
        "title": "Repeating Event",
        "start": "2026-06-16T16:00:00",
        "classNames": ["all"],
        "link": "https://www.marcelldls.lol/0",
    },
    {
        "title": "Conference",
        "start": "2026-06-11",
        "end": "2026-06-13",
        "classNames": ["all", "business", "personal"],
        "link": "https://www.marcelldls.lol/0",
    },
    {
        "title": "Meeting",
        "start": "2026-06-12T10:30:00",
        "end": "2026-06-12T12:30:00",
        "classNames": ["all"],
        "link": "https://www.marcelldls.lol/0",
    },
    {
        "title": "Lunch",
        "start": "2026-06-12T12:00:00",
        "classNames": ["all"],
        "link": "https://www.marcelldls.lol/0",
    },
    {
        "title": "Meeting",
        "start": "2026-06-12T14:30:00",
        "classNames": ["all"],
        "link": "https://www.marcelldls.lol/0",
    },
    {
        "title": "Birthday Party",
        "start": "2026-06-13T07:00:00",
        "classNames": ["all"],
        "link": "https://www.marcelldls.lol/0",
    },
    {
        "title": "Click for Google",
        "start": "2026-06-28",
        "classNames": ["all"],
        "link": "https://www.marcelldls.lol/0",
    },
    {
        "title": "Dentist Checkup",
        "start": "2026-06-25T10:00:00",
        "end": "2026-06-25T11:30:00",
        "classNames": ["all", "medical"],
        "link": "https://www.marcelldls.lol/0",
    },
    {
        "title": "Quarterly Board Meeting",
        "start": "2026-06-27T14:00:00",
        "end": "2026-06-27T16:00:00",
        "classNames": ["all", "business"],
        "link": "https://www.marcelldls.lol/0",
    },
    {
        "title": "Dinner with Parents",
        "start": "2026-06-29T19:00:00",
        "classNames": ["all", "personal", "medical"],
        "link": "https://www.marcelldls.lol/0",
    },
]

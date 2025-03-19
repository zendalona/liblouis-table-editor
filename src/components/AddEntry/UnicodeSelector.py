import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QTreeWidget, QTreeWidgetItem,
    QGridLayout, QScrollArea, QPushButton, QSizePolicy, QLineEdit, QTextEdit, QLabel
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont
from utils.ApplyStyles import apply_styles

class UnicodeSelector(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Unicode Character Map')
        self.selected_characters = []
        self.initUI()

    def initUI(self):
        main_layout = QHBoxLayout(self)

        search_layout = QVBoxLayout()
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search Unicode Blocks...")
        self.search_bar.textChanged.connect(self.filter_blocks)
        search_layout.addWidget(self.search_bar)

        self.tree = QTreeWidget()
        self.tree.setHeaderLabel("Unicode Blocks")
        self.populate_tree()
        self.tree.itemClicked.connect(self.display_characters)
        self.tree.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        search_layout.addWidget(self.tree)

        char_search_layout = QVBoxLayout()

        scroll_area = QScrollArea()
        self.char_container = QWidget()
        self.char_layout = QGridLayout(self.char_container)
        self.char_layout.setContentsMargins(0, 0, 0, 0)
        self.char_layout.setSpacing(0)
        self.char_container.setStyleSheet("background: white;")
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.char_container)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        char_search_layout.addWidget(scroll_area)

        self.selected_text_edit = QTextEdit()
        self.selected_text_edit.setFont(QFont('', 28))
        self.selected_text_edit.setPlaceholderText("Selected characters will appear here. You can also type in this box.")
        self.selected_text_edit.setFixedHeight(50)
        self.selected_text_edit.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.selected_text_edit.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        char_search_layout.addWidget(self.selected_text_edit)


        self.done_button = QPushButton("Done")
        self.done_button.clicked.connect(self.confirm_selection)
        char_search_layout.addWidget(self.done_button)

        main_layout.addLayout(search_layout)
        main_layout.addLayout(char_search_layout)

        self.setLayout(main_layout)
        self.setFixedSize(960, 600)

        self.adjust_component_sizes()

        if self.tree.topLevelItemCount() > 0:
            first_item = self.tree.topLevelItem(0)
            self.tree.setCurrentItem(first_item)
            self.display_characters(first_item, 0)
            
        apply_styles(self)


    def populate_tree(self):
        self.blocks = self.get_unicode_blocks()
        for block_name, (start, end) in self.blocks.items():
            item = QTreeWidgetItem([block_name])
            item.setData(0, Qt.ItemDataRole.UserRole, (start, end))
            self.tree.addTopLevelItem(item)

    def filter_blocks(self):
        search_text = self.search_bar.text().lower()
        for i in range(self.tree.topLevelItemCount()):
            item = self.tree.topLevelItem(i)
            item.setHidden(search_text not in item.text(0).lower())

    def get_unicode_blocks(self):
        return {
    "Adlam": (125184, 125279),
    "Aegean Numbers": (65792, 65855),
    "Ahom": (71424, 71487),
    "Alchemical Symbols": (128768, 128895),
    "Alphabetic Presentation Forms": (64256, 64335),
    "Anatolian Hieroglyphs": (82944, 83583),
    "Ancient Greek Musical Notation": (119296, 119375),
    "Ancient Greek Numbers": (65856, 65935),
    "Ancient Symbols": (65936, 65999),
    "Arabic": (1536, 1791),
    "Arabic Extended-A": (2208, 2303),
    "Arabic Extended-B": (2160, 2207),
    "Arabic Extended-C": (69312, 69375),
    "Arabic Mathematical Alphabetic Symbols": (126464, 126719),
    "Arabic Presentation Forms-A": (64336, 65023),
    "Arabic Presentation Forms-B": (65136, 65279),
    "Arabic Supplement": (1872, 1919),
    "Armenian": (1328, 1423),
    "Arrows": (8592, 8703),
    "Avestan": (68352, 68415),
    "Balinese": (6912, 7039),
    "Bamum": (42656, 42751),
    "Bamum Supplement": (92160, 92735),
    "Bassa Vah": (92880, 92927),
    "Batak": (7104, 7167),
    "Bengali": (2432, 2559),
    "Bhaiksuki": (72704, 72815),
    "Block Elements": (9600, 9631),
    "Bopomofo": (12544, 12591),
    "Bopomofo Extended": (12704, 12735),
    "Box Drawing": (9472, 9599),
    "Brahmi": (69632, 69759),
    "Braille Patterns": (10240, 10495),
    "Buginese": (6656, 6687),
    "Buhid": (5952, 5983),
    "Byzantine Musical Symbols": (118784, 119039),
    "C0 Controls and Basic Latin": (0, 127),
    "C1 Controls and Latin-1 Supplement": (128, 255),
    "CJK Compatibility": (13056, 13311),
    "CJK Compatibility Forms": (65072, 65103),
    "CJK Compatibility Ideographs": (63744, 64255),
    "CJK Compatibility Ideographs Supplement": (194560, 195103),
    "CJK Radicals Supplement": (11904, 12031),
    "CJK Strokes": (12736, 12783),
    "CJK Symbols and Punctuation": (12288, 12351),
    "CJK Unified Ideographs": (19968, 40959),
    "CJK Unified Ideographs Extension A": (13312, 19903),
    "CJK Unified Ideographs Extension B": (131072, 173791),
    "CJK Unified Ideographs Extension C": (173824, 177983),
    "CJK Unified Ideographs Extension D": (177984, 178207),
    "CJK Unified Ideographs Extension E": (178208, 183983),
    "CJK Unified Ideographs Extension F": (183984, 191471),
    "Carian": (66208, 66271),
    "Caucasian Albanian": (66864, 66927),
    "Chakma": (69888, 69967),
    "Cham": (43520, 43615),
    "Cherokee": (5024, 5119),
    "Cherokee Supplement": (43888, 43967),
    "Chess Symbols": (129536, 129647),
    "Chorasmian": (69552, 69599),
    "Combining Diacritical Marks": (768, 879),
    "Combining Diacritical Marks Extended": (6832, 6911),
    "Combining Diacritical Marks Supplement": (7616, 7679),
    "Combining Diacritical Marks for Symbols": (8400, 8447),
    "Combining Half Marks": (65056, 65071),
    "Common Indic Number Forms": (43056, 43071),
    "Control Pictures": (9216, 9279),
    "Coptic": (11392, 11519),
    "Coptic Epact Numbers": (66272, 66303),
    "Counting Rod Numerals": (119648, 119679),
    "Cuneiform": (73728, 74751),
    "Cuneiform Numbers and Punctuation": (74752, 74879),
    "Currency Symbols": (8352, 8399),
    "Cypriot Syllabary": (67584, 67647),
    "Cyrillic": (1024, 1279),
    "Cyrillic Extended-A": (11744, 11775),
    "Cyrillic Extended-B": (42560, 42655),
    "Cyrillic Extended-C": (7296, 7311),
    "Cyrillic Supplement": (1280, 1327),
    "Deseret": (66560, 66639),
    "Devanagari": (2304, 2431),
    "Devanagari Extended": (43232, 43263),
    "Dingbats": (9984, 10175),
    "Dogra": (71680, 71759),
    "Domino Tiles": (127024, 127135),
    "Duployan": (113664, 113823),
    "Early Dynastic Cuneiform": (74880, 75087),
    "Egyptian Hieroglyph Format Controls": (78896, 78911),
    "Egyptian Hieroglyphs": (77824, 78895),
    "Elbasan": (66816, 66863),
    "Elymaic": (69600, 69631),
    "Emoticons": (128512, 128591),
    "Enclosed Alphanumeric Supplement": (127232, 127487),
    "Enclosed Alphanumerics": (9312, 9471),
    "Enclosed CJK Letters and Months": (12800, 13055),
    "Enclosed Ideographic Supplement": (127488, 127743),
    "Ethiopic": (4608, 4991),
    "Ethiopic Extended": (11648, 11743),
    "Ethiopic Extended-A": (43776, 43823),
    "Ethiopic Extended-B": (124896, 124927),
    "Ethiopic Supplement": (4992, 5023),
    "General Punctuation": (8192, 8303),
    "Geometric Shapes": (9632, 9727),
    "Geometric Shapes Extended": (128896, 129023),
    "Georgian": (4256, 4351),
    "Georgian Extended": (7312, 7359),
    "Georgian Supplement": (11520, 11567),
    "Glagolitic": (11264, 11359),
    "Glagolitic Supplement": (122880, 122927),
    "Gothic": (66352, 66383),
    "Grantha": (70400, 70527),
    "Greek Extended": (7936, 8191),
    "Greek and Coptic": (880, 1023),
    "Gujarati": (2688, 2815),
    "Gunjala Gondi": (73056, 73135),
    "Gurmukhi": (2560, 2687),
    "Halfwidth and Fullwidth Forms": (65280, 65519),
    "Hangul Compatibility Jamo": (12592, 12687),
    "Hangul Jamo": (4352, 4607),
    "Hangul Jamo Extended-A": (43360, 43391),
    "Hangul Jamo Extended-B": (55216, 55295),
    "Hangul Syllables": (44032, 55215),
    "Hanifi Rohingya": (68864, 68927),
    "Hanunoo": (5920, 5951),
    "Hatran": (67808, 67839),
    "Hebrew": (1424, 1535),
    "High Private Use Surrogates": (56192, 56319),
    "High Surrogates": (55296, 56191),
    "Hiragana": (12352, 12447),
    "IPA Extensions": (592, 687),
    "Ideographic Description Characters": (12272, 12287),
    "Ideographic Symbols and Punctuation": (94176, 94207),
    "Imperial Aramaic": (67648, 67679),
    "Indic Siyaq Numbers": (126064, 126143),
    "Inscriptional Pahlavi": (68448, 68479),
    "Inscriptional Parthian": (68416, 68447),
    "Javanese": (43392, 43487),
    "Kaithi": (69760, 69839),
    "Kana Extended-A": (110848, 110895),
    "Kana Supplement": (110592, 110847),
    "Kanbun": (12688, 12703),
    "Kangxi Radicals": (12032, 12255),
    "Kannada": (3200, 3327),
    "Katakana": (12448, 12543),
    "Katakana Phonetic Extensions": (12784, 12799),
    "Kayah Li": (43264, 43311),
    "Kharoshthi": (68096, 68191),
    "Khmer": (6016, 6143),
    "Khmer Symbols": (6624, 6655),
    "Khojki": (70144, 70223),
    "Khudawadi": (70320, 70399),
    "Lao": (3712, 3839),
    "Latin Extended Additional": (7680, 7935),
    "Latin Extended-A": (256, 383),
    "Latin Extended-B": (384, 591),
    "Latin Extended-C": (11360, 11391),
    "Latin Extended-D": (42784, 43007),
    "Latin Extended-E": (43824, 43887),
    "Latin Extended-F": (67456, 67519),
    "Lepcha": (7168, 7247),
    "Letterlike Symbols": (8448, 8527),
    "Limbu": (6400, 6479),
    "Linear A": (67072, 67455),
    "Linear B Ideograms": (65664, 65791),
    "Linear B Syllabary": (65536, 65663),
    "Lisu": (42192, 42239),
    "Low Surrogates": (56320, 57343),
    "Lycian": (66176, 66207),
    "Lydian": (67872, 67903),
    "Mahajani": (69968, 70015),
    "Mahjong Tiles": (126976, 127023),
    "Makasar": (73440, 73471),
    "Malayalam": (3328, 3455),
    "Mandaic": (2112, 2143),
    "Manichaean": (68288, 68351),
    "Marchen": (72816, 72895),
    "Masaram Gondi": (72960, 73055),
    "Mathematical Alphanumeric Symbols": (119808, 120831),
    "Mathematical Operators": (8704, 8959),
    "Mayan Numerals": (119520, 119551),
    "Medefaidrin": (93760, 93855),
    "Meetei Mayek": (43968, 44031),
    "Meetei Mayek Extensions": (43744, 43775),
    "Mende Kikakui": (124928, 125151),
    "Meroitic Cursive": (68000, 68095),
    "Meroitic Hieroglyphs": (67968, 67999),
    "Miao": (93952, 94111),
    "Miscellaneous Mathematical Symbols-A": (10176, 10223),
    "Miscellaneous Mathematical Symbols-B": (10624, 10751),
    "Miscellaneous Symbols": (9728, 9983),
    "Miscellaneous Symbols and Arrows": (11008, 11263),
    "Miscellaneous Symbols and Pictographs": (127744, 128511),
    "Miscellaneous Technical": (8960, 9215),
    "Modi": (71168, 71263),
    "Modifier Tone Letters": (42752, 42783),
    "Mongolian": (6144, 6319),
    "Mongolian Supplement": (71264, 71295),
    "Mro": (92736, 92783),
    "Multani": (70272, 70319),
    "Musical Symbols": (119040, 119295),
    "Myanmar": (4096, 4255),
    "Myanmar Extended-A": (43616, 43647),
    "Myanmar Extended-B": (43488, 43519),
    "NKo": (1984, 2047),
    "Nabataean": (67712, 67759),
    "Nandinagari": (72096, 72191),
    "New Tai Lue": (6528, 6623),
    "Newa": (70656, 70783),
    "Number Forms": (8528, 8591),
    "Nushu": (110960, 111359),
    "Nyiakeng Puachue Hmong": (123136, 123215),
    "Ogham": (5760, 5791),
    "Ol Chiki": (7248, 7295),
    "Old Hungarian": (68736, 68863),
    "Old Italic": (66304, 66351),
    "Old North Arabian": (68224, 68255),
    "Old Permic": (66384, 66431),
    "Old Persian": (66464, 66527),
    "Old Sogdian": (69376, 69423),
    "Old South Arabian": (68192, 68223),
    "Old Turkic": (68608, 68687),
    "Old Uyghur": (69488, 69551),
    "Optical Character Recognition": (9280, 9311),
    "Oriya": (2816, 2943),
    "Ornamental Dingbats": (128592, 128639),
    "Osage": (66736, 66815),
    "Osmanya": (66688, 66735),
    "Ottoman Siyaq Numbers": (126208, 126287),
    "Pahawh Hmong": (92928, 93071),
    "Palmyrene": (67680, 67711),
    "Pau Cin Hau": (72384, 72447),
    "Phags-pa": (43072, 43135),
    "Phaistos Disc": (66000, 66047),
    "Phoenician": (67840, 67871),
    "Phonetic Extensions": (7424, 7551),
    "Phonetic Extensions Supplement": (7552, 7615),
    "Playing Cards": (127136, 127231),
    "Private Use Area": (57344, 63743),
    "Psalter Pahlavi": (68480, 68527),
    "Rejang": (43312, 43359),
    "Rumi Numeral Symbols": (69216, 69247),
    "Runic": (5792, 5887),
    "Samaritan": (2048, 2111),
    "Saurashtra": (43136, 43231),
    "Sharada": (70016, 70111),
    "Shavian": (66640, 66687),
    "Shorthand Format Controls": (113824, 113839),
    "Siddham": (71040, 71167),
    "Sinhala": (3456, 3583),
    "Sinhala Archaic Numbers": (70112, 70143),
    "Small Form Variants": (65104, 65135),
    "Small Kana Extension": (110896, 110959),
    "Sogdian": (69424, 69487),
    "Sora Sompeng": (69840, 69887),
    "Soyombo": (72272, 72367),
    "Spacing Modifier Letters": (688, 767),
    "Specials": (65520, 65535),
    "Sundanese": (7040, 7103),
    "Sundanese Supplement": (7360, 7375),
    "Superscripts and Subscripts": (8304, 8351),
    "Supplemental Arrows-A": (10224, 10239),
    "Supplemental Arrows-B": (10496, 10623),
    "Supplemental Arrows-C": (129024, 129279),
    "Supplemental Mathematical Operators": (10752, 11007),
    "Supplemental Punctuation": (11776, 11903),
    "Supplemental Symbols and Pictographs": (129280, 129535),
    "Supplementary Private Use Area-A": (983040, 1048575),
    "Supplementary Private Use Area-B": (1048576, 1114111),
    "Sutton SignWriting": (120832, 121519),
    "Syloti Nagri": (43008, 43055),
    "Symbols and Pictographs Extended-A": (129648, 129791),
    "Syriac": (1792, 1871),
    "Syriac Supplement": (2144, 2159),
    "Tagalog": (5888, 5919),
    "Tagbanwa": (5984, 6015),
    "Tags": (917504, 917631),
    "Tai Le": (6480, 6527),
    "Tai Tham": (6688, 6831),
    "Tai Viet": (43648, 43743),
    "Tai Xuan Jing Symbols": (119552, 119647),
    "Takri": (71296, 71375),
    "Tamil": (2944, 3071),
    "Tamil Supplement": (73664, 73727),
    "Tangut": (94208, 100351),
    "Tangut Components": (100352, 101119),
    "Telugu": (3072, 3199),
    "Thaana": (1920, 1983),
    "Thai": (3584, 3711),
    "Tibetan": (3840, 4095),
    "Tifinagh": (11568, 11647),
    "Tirhuta": (70784, 70879),
    "Toto": (123536, 123583),
    "Transport and Map Symbols": (128640, 128767),
    "Ugaritic": (66432, 66463),
    "Unified Canadian Aboriginal Syllabics": (5120, 5759),
    "Unified Canadian Aboriginal Syllabics Extended": (6320, 6399),
    "Vai": (42240, 42559),
    "Variation Selectors": (65024, 65039),
    "Variation Selectors Supplement": (917760, 917999),
    "Vedic Extensions": (7376, 7423),
    "Vertical Forms": (65040, 65055),
    "Vithkuqi": (66928, 67007),
    "Wancho": (123584, 123647),
    "Warang Citi": (71840, 71935),
    "Yezidi": (69248, 69311),
    "Yi Radicals": (42128, 42191),
    "Yi Syllables": (40960, 42127),
    "Yijing Hexagram Symbols": (19904, 19967),
    "Zanabazar Square": (72192, 72271),
}

    def display_characters(self, item, column):
        while self.char_layout.count():
            child = self.char_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        start, end = item.data(0, Qt.ItemDataRole.UserRole)
        self.characters = [chr(codepoint) for codepoint in range(start, end + 1)]

        self.update_character_display()

    def update_character_display(self):
        button_size = 80
        padding = 2
        available_width = self.width() - self.tree.sizeHint().width() - padding * 2
        num_columns = available_width // button_size

        if num_columns < 1:
            num_columns = 1

        num_rows = (len(self.characters) + num_columns - 1) // num_columns

        container_width = num_columns * button_size
        container_height = num_rows * button_size

        self.char_container.setFixedSize(container_width, container_height)

        for row in range(num_rows):
            for col in range(num_columns):
                index = row * num_columns + col
                if index >= len(self.characters):
                    break

                char = self.characters[index]
                char_button = QPushButton(char)
                char_button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
                char_button.setFixedSize(QSize(button_size, button_size))

                char_button.setStyleSheet(
                    "QPushButton {"
                    "    font-size: 32px;"
                    "    font-weight: lighter;"
                    "    background: white;"
                    
                    "}"
                    "QPushButton:hover {"
                    "    background: #d4e9f7;"
                    "}"
                )
                char_button.clicked.connect(self.character_selected)
                self.char_layout.addWidget(char_button, row, col)

    def character_selected(self):
        char_button = self.sender()
        selected_char = char_button.text()

        self.selected_characters.append(selected_char)

        self.selected_text_edit.setPlainText("".join(self.selected_characters))

    def confirm_selection(self):
        manual_input = self.selected_text_edit.toPlainText()
        selected_string = "".join(self.selected_characters) + manual_input

        selected_string = "".join(sorted(set(selected_string), key=selected_string.index))

        if self.on_select_callback:
            hex_representation = "\\x" + "\\x".join(f"{ord(char):04X}" for char in selected_string)
            self.on_select_callback(selected_string, hex_representation)
        self.close()

    def on_select(self, callback):
        self.on_select_callback = callback

    def adjust_component_sizes(self):
        self.tree.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.char_container.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

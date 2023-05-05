import guilded
from guilded.ext import commands
import json
import uuid
from tools.dataIO import fileIO
import re
from core.database import *
import psycopg
from psycopg_pool import ConnectionPool 
from tools.db_funcs import getServer
from tools.db_funcs import getUser
from tools.db_funcs import getUserLB
from psycopg.rows import dict_row

def remove_repeated_letters(word):
    return re.sub(r'(.)\1+', r'\1', word)

def generate_combinations(word, char_mapping):
    if not word:
        return ['']

    head, *tail = word
    tail_combinations = generate_combinations(tail, char_mapping)

    if head in char_mapping:
        substitutions = char_mapping[head]
        return [c + tail_comb for c in substitutions for tail_comb in tail_combinations]
    else:
        return [head + tail_comb for tail_comb in tail_combinations]

def clean_word(word, char_mapping):

	word = remove_repeated_letters(word)

	char_mapping = {
        "a": ["4", "Á", "ą,", "á", "À", "à", "Â", "â", "Ã", "ã", "Ä", "ä", "Å", "å", "ạ", "Ȧ", "ȧ", "ǎ", "Ǎ", "Ȁ", "ȁ", "Ȃ", "ȃ", "Ạ", "ạ", "ⓐ", "Ⓐ", "₳", "α", "Α", "ａ", "Ａ", "ª", "ä", "Ä", "⍺", "𝐚", "𝐀", "𝐚", "𝐀", "𝑎", "𝑨", "𝒂", "𝑨", "𝒜", "𝒶", "𝓪", "𝓐", "𝓪", "𝓐", "𝔞", "𝔄", "𝔞", "𝔸", "𝕒", "𝕬", "𝖆", "𝖠", "𝖺", "𝗮", "𝗔", "𝗮", "𝗔", "𝘢", "𝘈", "𝘢", "𝘼", "𝙖", "𝘼", "𝙖", "𝘼", "𝚊", "𝙰", "𝚊", "𝚨"],
		"b": ["8", "6", "ß", "Β", "β", "฿", "ҍ", "Ϧ", "þ", "ҭ", "ƀ", "Ɓ", "Ƀ", "ɓ", "ɓ", "ɞ", "ʙ", "ᛒ", "Ｂ", "ｂ", "𝐛", "𝐁", "𝐛", "𝐁", "𝑏", "𝑩", "𝒃", "𝑩", "𝓫", "𝓑", "𝓫", "𝓑", "𝔟", "𝔅", "𝔟", "𝔹", "𝕓", "𝕭", "𝖇", "𝕯", "𝖡", "𝖻", "𝗯", "𝗕", "𝗯", "𝗕", "𝘣", "𝘉", "𝘣", "𝘽", "𝙗", "𝘽", "𝙗", "𝘽", "𝚋", "𝙱", "𝚋", "𝚩"],
		"c": ["(", "[", "{", "<", "©", "¢", "Ƈ", "ƈ", "Ȼ", "ȼ", "ϲ", "Ϲ", "Ͻ", "ℂ", "ℭ", "Ⅽ", "ⅽ", "ⅽ", "ⅽ", "ｃ", "Ｃ", "𝐜", "𝐂", "𝐜", "𝐂", "𝑐", "𝐂", "𝒄", "𝐂", "𝒞", "𝒸", "𝓬", "𝓒", "𝓬", "𝓒", "𝔠", "𝕮", "𝖈", "𝕮", "𝖢", "𝖼", "𝗰", "𝗖", "𝗰", "𝗖", "𝘤", "𝘊", "𝘤", "𝘾", "𝙘", "𝘾", "𝙘", "𝘾", "𝚌", "𝙲", "𝚌"],
		"d": [")", "]", "}", "|)", "|]", "⟩", "₫", "Ɖ", "ɖ", "ȡ", "ᑯ", "ᒣ", "ḍ", "Ḏ", "ḏ", "Ḑ", "ḑ", "Ḓ", "ḓ", "ḓ", "ⅆ", "ｄ", "Ｄ", "𝐝", "𝐃", "𝐝", "𝐃", "𝑑", "𝐃", "𝒅", "𝐃", "𝒟", "𝒹", "𝓭", "𝓓", "𝓭", "𝓓", "𝔡", "𝕯", "𝖉", "𝕯", "𝖣", "𝖽", "𝗱", "𝗗", "𝗱", "𝗗", "𝘥", "𝘋", "𝘥", "𝘿", "𝙙", "𝘿", "𝙙", "𝘿", "𝚍", "𝙳", "𝚍", "𝚫"],
		"e": ["3", "€", "ë", "Ë", "ē", "Ē", "ĕ", "Ĕ", "ė", "Ė", "ě", "Ě", "ȅ", "Ȅ", "ȇ", "Ȇ", "ẹ", "Ẹ", "ę", "Ę", "ɛ", "Ɛ", "ǝ", "ɘ", "ℇ", "℮", "∃", "⋿", "ｅ", "Ｅ", "𝐞", "𝐄", "𝐞", "𝐄", "𝑒", "𝐄", "𝒆", "𝐄", "ℰ", "𝓮", "𝓔", "𝓮", "𝓔", "𝔢", "𝕰", "𝖊", "𝕰", "𝖤", "𝖾", "𝗲", "𝗘", "𝗲", "𝗘", "𝘦", "𝘌", "𝘦", "𝙀", "𝙚", "𝙀", "𝙚", "𝙀", "𝚎", "𝙴", "𝚎", "𝚬", "ₑ"],
		"f": ["ƒ", "ſ", "Ⓕ", "𝔣", "𝕗", "𝔽", "𝖋", "𝕱", "𝖥", "𝗳", "𝗙", "𝗳", "𝗙", "𝘧", "𝘍", "𝘧", "𝙁", "𝙛", "𝙁", "𝙛", "𝙁", "𝚏", "𝙵"],
		"g": ["9", "6", "ɡ", "ɢ", "₲", "ℊ", "ℊ", "Ⓖ", "ǥ", "Ǥ", "ɠ", "ɡ", "ɢ", "Ꮆ", "Ꮆ", "ℊ", "𝔤", "𝕘", "𝔾", "𝖌", "𝕲", "𝖦", "𝗀", "𝗴", "𝗚", "𝗴", "𝗚", "𝘨", "𝘎", "𝘨", "𝙂", "𝙜", "𝙂", "𝙜", "𝙂", "𝚐", "𝙶", "𝚐"],
		"h": ["#", "Ħ", "ħ", "Ȟ", "ȟ", "ĥ", "Ĥ", "Ḩ", "ḩ", "Ḥ", "ḥ", "Ḧ", "ḧ", "Ḫ", "ḫ", "Ⱨ", "ⱨ", "ｈ", "Ｈ", "𝐡", "𝐇", "𝐡", "𝐇", "𝒉", "𝐇", "𝒽", "𝐇", "ℋ", "𝓱", "𝓗", "𝓱", "𝓗", "𝔥", "𝕳", "𝖍", "𝕳", "𝖧", "𝗁", "𝗛", "𝗁", "𝗛", "𝘩", "𝘏", "𝘩", "𝙃", "𝙝", "𝙃", "𝙝", "𝙃", "𝚑", "𝙷", "𝚑", "ℎ"],
		"i": ["1", "!", "|", "į", "]", "[", "}", "{", ")", "(", "Ꭵ", "ᶦ", "ï", "Î", "î", "Ï", "í", "Í", "ĭ", "Ĭ", "ǐ", "Ǐ", "ȉ", "Ȉ", "ȋ", "Ȋ", "ɪ", "İ", "ι", "ί", "Ι", "ｉ", "Ｉ", "𝐢", "𝐈", "𝐢", "𝐈", "𝑖", "𝐈", "𝒊", "𝐈", "ℐ", "𝓲", "𝓘", "𝓲", "𝓘", "𝔦", "𝕴", "𝖎", "𝕴", "𝖨", "𝗂", "𝗜", "𝗂", "𝗜", "𝘪", "𝘐", "𝘪", "𝙄", "𝙞", "𝙄", "𝙞", "𝙄", "𝚒", "𝙸", "𝚒"],
		"j": ["ʝ", "ϳ", "ĵ", "Ĵ", "ǰ", "Ǧ", "ȷ", "ɉ", "Ɉ", "ʲ", "ʝ", "ⅉ", "ｊ", "Ｊ", "𝐣", "𝐉", "𝐣", "𝐉", "𝑗", "𝐉", "𝒋", "𝐉", "𝒥", "𝒿", "𝓳", "𝓙", "𝓳", "𝓙", "𝔧", "𝕵", "𝖏", "𝕵", "𝖩", "𝗃", "𝗝", "𝗃", "𝗝", "𝘫", "𝘑", "𝘫", "𝙅", "𝙟", "𝙅", "𝙟", "𝙅", "𝚓", "𝙹", "𝚓"],
		"k": ["κ", "ķ", "Ķ", "Ƙ", "ƙ", "Ḳ", "ḳ", "Ḵ", "ḵ", "Ⱪ", "ⱪ", "ｋ", "Ｋ", "𝐤", "𝐊", "𝐤", "𝐊", "𝑘", "𝐊", "𝒌", "𝐊", "𝒦", "𝓀", "𝓚", "𝓴", "𝓚", "𝓴", "𝔨", "𝕶", "𝖐", "𝕶", "𝖪", "𝗄", "𝗞", "𝗄", "𝗞", "𝗸", "𝗞", "𝘬", "𝙆", "𝙠", "𝙆", "𝙠", "𝙆", "𝚔", "𝙺", "𝚔"],
		"l": ["1", "!", "į", "|", "]", "[", "}", "{", "7", "ł", "Ł", "Ĺ", "ĺ", "Ļ", "ļ", "Ḷ", "ḷ", "Ḹ", "ḹ", "Ⱡ", "Ɫ", "ｌ", "Ｌ", "𝐥", "𝐋", "𝐥", "𝐋", "𝑙", "𝐋", "𝒍", "𝐋", "ℒ", "𝓁", "𝓛", "𝓵", "𝓛", "𝓵", "𝔩", "𝕷", "𝖑", "𝕷", "𝖫", "𝗅", "𝗟", "𝗅", "𝗟", "𝗹", "𝗟", "𝘭", "𝙇", "𝙡", "𝙇", "𝙡", "𝙇", "𝚕", "𝙻", "𝚕"],
		"m": ["₥", "ᗰ", "ᙢ", "ᙣ", "Ḿ", "ḿ", "Ṁ", "ṁ", "Ṃ", "ṃ", "ɱ", "Ⓜ", "ｍ", "Ｍ", "𝐦", "𝐌", "𝐦", "𝐌", "𝑚", "𝐌", "𝒎", "𝐌", "ℳ", "𝓂", "𝓜", "𝓶", "𝓜", "𝓶", "𝔪", "𝕸", "𝖒", "𝕸", "𝖬", "𝗆", "𝗠", "𝗆", "𝗠", "𝗺", "𝗠", "𝘮", "𝙈", "𝙢", "𝙈", "𝙢", "𝙈", "𝚖", "𝙼", "𝚖"],
		"n": ["η", "π", "ñ", "Ñ", "ń", "Ń", "Ņ", "ņ", "Ň", "ň", "Ŋ", "ŋ", "ɴ", "₦", "ｎ", "Ｎ", "𝐧", "𝐍", "𝐧", "𝐍", "𝑛", "𝐍", "𝒏", "𝐍", "𝒩", "𝓃", "𝓝", "𝓷", "𝓝", "𝓷", "𝔫", "𝕹", "𝖓", "𝕹", "𝖭", "𝗇", "𝗡", "𝗇", "𝗡", "𝗻", "𝗡", "𝘯", "𝙉", "𝙣", "𝙉", "𝙣", "𝙉", "𝚗", "𝙽", "𝚗"],
		"o": ["0", "⊕", "ø", "Ø", "ö", "Ö", "ó", "Ó", "ò", "Ò", "ô", "Ô", "õ", "Õ", "ō", "Ō", "ȯ", "Ȯ", "Ȱ", "ȱ", "ɵ", "ɔ", "ⓞ", "ｏ", "Ｏ", "𝐨", "𝐎", "𝐨", "𝐎", "𝑜", "𝐎", "𝒐", "𝐎", "𝒪", "𝓸", "𝓞", "𝓸", "𝓞", "𝔬", "𝕺", "𝖔", "𝕺", "𝖮", "𝗈", "𝗢", "𝗈", "𝗢", "𝗼", "𝗢", "𝘰", "𝙊", "𝙤", "𝙊", "𝙤", "𝙊", "𝚘", "𝙾", "𝚘", "ο"],
		"p": ["ρ", "Р", "р", "Ṗ", "ṗ", "Ṕ", "ṕ", "Ⓟ", "ｐ", "Ｐ", "𝐩", "𝐏", "𝐩", "𝐏", "𝑝", "𝐏", "𝒑", "𝐏", "𝒫", "𝓅", "𝓟", "𝓹", "𝓟", "𝓹", "𝔭", "𝕻", "𝖕", "𝕻", "𝖯", "𝗉", "𝗣", "𝗉", "𝗣", "𝗽", "𝗣", "𝘱", "𝙋", "𝙥", "𝙋", "𝙥", "𝙋", "𝚙", "𝙿", "𝚙"],
		"q": ["q", "𝐪", "𝐐", "𝐪", "𝐐", "𝑞", "𝐐", "𝒒", "𝐐", "𝒬", "𝓆", "𝓠", "𝓺", "𝓠", "𝓺", "𝔮", "𝕼", "𝖖", "𝕼", "𝖰", "𝗊", "𝗤", "𝗊", "𝗤", "𝗾", "𝗤", "𝘲", "𝙌", "𝙦", "𝙌", "𝙦", "𝙌", "𝚚", "𝚀", "𝚚"],
		"r": ["®", "Ṛ", "ṛ", "Ṝ", "ṝ", "Ṟ", "ṟ", "ɾ", "ɼ", "ɽ", "ɿ", "Ⓡ", "ｒ", "Ｒ", "𝐫", "𝐑", "𝐫", "𝐑", "𝑟", "𝐑", "𝒓", "𝐑", "ℛ", "𝓇", "𝓡", "𝓻", "𝓡", "𝓻", "𝔯", "𝕽", "𝖗", "𝕽", "𝖱", "𝗋", "𝗥", "𝗋", "𝗥", "𝗿", "𝗥", "𝘳", "𝙍", "𝙧", "𝙍", "𝙧", "𝙍", "𝚛", "𝚁", "𝚛"],
		"s": ["5", "$", "§", "Ş", "ş", "Š", "š", "Ṡ", "ṡ", "Ṣ", "ṣ", "Ṥ", "ṥ", "Ⓢ", "ｓ", "Ｓ", "𝐬", "𝐒", "𝐬", "𝐒", "𝑠", "𝐒", "𝒔", "𝐒", "𝒮", "𝓈", "𝓢", "𝓼", "𝓢", "𝓼", "𝔰", "𝕾", "𝖘", "𝕾", "𝖲", "𝗌", "𝗦", "𝗌", "𝗦", "𝘀", "𝗦", "𝘀", "𝙎", "𝙨", "𝙎", "𝙨", "𝙎", "𝚜", "𝚂", "𝚜"],
		"t": ["7", "+", "†", "ţ", "Ţ", "ť", "Ť", "Ŧ", "ŧ", "ƫ", "Ƭ", "ƭ", "Ʈ", "Ⓣ", "ｔ", "Ｔ", "𝐭", "𝐓", "𝐭", "𝐓", "𝑡", "𝐓", "𝒕", "𝐓", "𝒯", "𝓉", "𝓣", "𝓽", "𝓣", "𝓽", "𝔱", "𝕋", "𝖙", "𝕋", "𝖳", "𝗍", "𝗧", "𝗍", "𝗧", "𝘁", "𝗧", "𝘁", "𝙏", "𝙩", "𝙏", "𝙩", "𝚝", "𝚃", "𝚝"],
		"u": ["μ", "ù", "Ù", "ú", "Ú", "û", "Û", "ü", "Ü", "Ũ", "ũ", "Ū", "ū", "Ŭ", "ŭ", "Ů", "ů", "Ű", "ű", "Ų", "ų", "ư", "Ư", "Ǔ", "ǔ", "Ǖ", "ǖ", "Ǘ", "ǘ", "Ǚ", "ǚ", "Ǜ", "ǜ", "ȕ", "Ȗ", "Ʉ", "Ⓤ", "ｕ", "Ｕ", "𝐮", "𝐔", "𝐮", "𝐔", "𝑢", "𝐔", "𝒖", "𝐔", "𝒰", "𝓊", "𝓤", "𝓾", "𝓤", "𝓾", "𝔲", "𝕌", "𝖚", "𝕌", "𝖴", "𝗎", "𝗨", "𝗎", "𝗨", "𝘂", "𝗨", "𝘂", "𝙐", "𝙪", "𝙐", "𝙪", "𝙐", "𝚞", "𝚄", "𝚞"],
		"v": ["ν", "Ṽ", "ṽ", "Ṿ", "ṿ", "Ⓥ", "ｖ", "Ｖ", "𝐯", "𝐕", "𝐯", "𝐕", "𝑣", "𝐕", "𝒗", "𝐕", "𝒱", "𝓋", "𝓥", "𝓿", "𝓥", "𝓿", "𝔳", "𝕍", "𝖛", "𝕍", "𝖵", "𝗏", "𝖵", "𝗏", "𝖶", "𝗩", "𝘃", "𝗩", "𝘷", "𝘝", "𝗺", "𝗠", "𝘷", "𝗠", "𝘝", "𝘷", "𝙑", "𝙫", "𝙑", "𝙫", "𝙑", "𝚟", "𝚅", "𝚟"],
		"w": ["ω", "ẁ", "Ẁ", "ẃ", "Ẃ", "ẅ", "Ẅ", "Ẇ", "ẇ", "Ẉ", "ẉ", "Ẋ", "ẋ", "Ⓦ", "ｗ", "Ｗ", "𝐰", "𝐖", "𝐰", "𝐖", "𝑤", "𝐖", "𝒘", "𝐖", "𝒲", "𝓌", "𝓦", "𝔀", "𝓦", "𝔀", "𝔴", "𝕎", "𝖜", "𝕎", "𝖶", "𝗐", "𝗪", "𝗐", "𝗪", "𝘄", "𝗪", "𝘄", "𝙒", "𝙬", "𝙒", "𝙬", "𝙒", "𝚠", "𝚆", "𝚠"],
		"x": ["×", "Ẋ", "ẋ", "Ẍ", "ẍ", "Ⓧ", "ｘ", "Ｘ", "𝐱", "𝐗", "𝐱", "𝐗", "𝑥", "𝐗", "𝒙", "𝐗", "𝒳", "𝓍", "𝓧", "𝔁", "𝓧", "𝔁", "𝔵", "𝕏", "𝖝", "𝕏", "𝖷", "𝗑", "𝗫", "𝗑", "𝗫", "𝘅", "𝗫", "𝘅", "𝙓", "𝙭", "𝙓", "𝙭", "𝙓", "𝚡", "𝚇", "𝚡"],
		"y": ["γ", "ÿ", "Ÿ", "ý", "Ý", "ŷ", "Ŷ", "Ȳ", "ȳ", "ɏ", "Ƴ", "ƴ", "¥", "Ⓨ", "ｙ", "Ｙ", "𝐲", "𝐘", "𝐲", "𝐘", "𝑦", "𝐘", "𝒚", "𝐘", "𝒴", "𝓎", "𝓨", "𝔂", "𝓨", "𝔂", "𝔶", "𝕐", "𝖞", "𝕐", "𝖸", "𝗒", "𝗬", "𝗒", "𝗬", "𝘆", "𝗬", "𝘆", "𝙔", "𝙮", "𝙔", "𝙮", "𝙔", "𝚢", "𝚈", "𝚢"],
		"z": ["ζ", "ź", "Ź", "ż", "Ż", "ž", "Ž", "Ẑ", "ẑ", "Ẓ", "ẓ", "Ẕ", "ẕ", "Ⓩ", "ｚ", "Ｚ", "𝐳", "𝐙", "𝐳", "𝐙", "𝑧", "𝐙", "𝒛", "𝐙", "𝒵", "𝓏", "𝓩", "𝔃", "𝓩", "𝔃", "𝔷", "𝖅", "𝖟", "𝖅", "𝖹", "𝗓", "𝗭", "𝗓", "𝗭", "𝘇", "𝗭", "𝘇", "𝙕", "𝙯", "𝙕", "𝙯", "𝙕", "𝚣", "𝚉", "𝚣"]
    }
	return [comb for comb in generate_combinations(word, char_mapping) if ' ' not in comb]

class Generator(commands.Cog):
	def __init__(self,bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_member_remove(self, event: guilded.MemberRemoveEvent):
		author = event.member
		guild = event.server
		kicked = event.kicked
		banned = event.banned
		if author.bot:
			return
		await _check_values_guild(guild)
		server = await getServer(guild.id)
		if server["log_actions"] == None:
			return
		if banned == True:
			channel = await guild.fetch_channel(server["log_actions"])
			em = guilded.Embed(title="A member was banned:", description="`Username:` {}\n`User ID:` {}".format(author.name, author.id), color=0x363942)
			await channel.send(embed=em)
		elif kicked  == True:
			channel = await guild.fetch_channel(server["log_actions"])
			em = guilded.Embed(title="A member was kicked:", description="`Username:` {}\n`User ID:` {}".format(author.name, author.id), color=0x363942)
			await channel.send(embed=em)
		else:
			channel = await guild.fetch_channel(server["log_traffic"])
			em = guilded.Embed(title="A member has left:", description="`Username:` {}\n`User ID:` {}".format(author.name, author.id), color=0x363942)
			await channel.send(embed=em)

	@commands.Cog.listener()
	async def on_bot_add(self, event: guilded.BotAddEvent):
		guild = event.server
		user = event.member
		author = user
		await _check_values(author)
		await _check_values_guild(guild)
		await check_leaderboard(author)
		await _check_inventory(author)
		send_channel = await guild.fetch_default_channel()
		support_guild = await self.bot.fetch_server("Mldgz04R")
		channel = await support_guild.fetch_channel("fd818fb2-c102-4ce9-b347-23d00a5649f8")
		await _check_values_guild(guild)
		em = guilded.Embed(title="Hello community!", description="`-` Thanks <@{}> for inviting me to **{}!**\n`-` My default prefix/help command is `?help`\n`-` Rayz is a multipurpose bot featuring moderation, logging, a global economy, interaction commands, and more!\n\n**Links**\n[Support server](https://guilded.gg/Rayz) • [Invite Rayz](https://www.guilded.gg/b/acd5fc8c-4272-48d0-b78b-da1fecb1bab5)".format(user.id, guild.name), color=0x363942)
		await send_channel.send(embed=em)
		em = guilded.Embed(title="Rayz joined a Guild!", description="**__{}__**\n**Inivted by:** `{} ({})`".format(guild.name, user.name, user.id), color=0x363942)
		await channel.send(embed=em)

	@commands.Cog.listener()
	async def on_member_join(self, event: guilded.MemberJoinEvent):
		author = event.member
		guild = event.server
		if author.bot:
			return
		await _check_values_guild(guild)
		server = await getServer(guild.id)
		if server["welcome_channel"] == None:
			pass
		else:
			try:
				channel = await guild.fetch_channel(server["welcome_channel"])
				if server["welcome_message"] == None:
					welcome_message = f"Welcome <@{author.id}> to {guild.name}!"
				else:
					welcome_message = server["welcome_message"]
				try:
					welcome_message = welcome_message.replace("<user>", f"<@{author.id}>")
				except:
					pass
				try:
					welcome_message = welcome_message.replace("<server>", f"{guild.name}")
				except:
					pass
				em = guilded.Embed(title="A member has joined!", description="{}".format(welcome_message), color=0x363942)
				try:
					em.set_thumbnail(url=guild.icon)
				except:
					pass
				await channel.send(embed=em)
			except:
				pass
			if server["log_traffic"] == None:
				pass
			else:
				channel = await guild.fetch_channel(server["log_traffic"])
				em = guilded.Embed(title="A member has joined:", description="`Username:` {}\n`User ID:` {}".format(author.name, author.id), color=0x363942)
				await channel.send(embed=em)

	@commands.Cog.listener()
	async def on_message(self, event: guilded.MessageEvent):
		author = event.message.author
		guild = event.server
		message = event.message
		if event.message.created_by_bot:
			return
		await _check_values(author)
		await _check_values_guild(guild)
		await check_leaderboard(author)
		await check_leaderboard_author(author)
		info = fileIO("config/banned_words.json", "load")

		server = await getServer(guild.id)
		prefix = server["server_prefix"]
		if server["custom_blocked_words"] == None:
			append_it = ["111111111111111111111111111111111111111111111111111111111111111111111111111111111"]
		else:
			append_it = server["custom_blocked_words"]
		swearwords = info["banned_words"] + append_it
		message_safe = True
		things_said = []
		captures = []
		for word in swearwords:
			if re.search(word, message.content.lower()):
				things_said.append("{}{}-".format(word[0], word[1]))
				captures.append(word)
				message_safe = False
		if not message_safe:
			moderator_or_not = False
			for i in author.roles:
				if i.permissions.manage_messages == True or i.permissions.kick_members == True:
					moderator_or_not = True
					await message.add_reaction(90002078)
			if moderator_or_not == False:
				if server["logs_channel_id"] == "None":
					em = guilded.Embed(title="A blacklisted word was used.", description="<@{}> **said:**\n{}".format(author.id, " \n".join(things_said)), color=0x363942)
					em.set_footer(icon_url= "https://img.guildedcdn.com/WebhookThumbnail/aa4b19b0bf393ca43b2f123c22deb94e-Full.webp?w=160&h=160s", text="Make sure to set a log channel to get the full details next time.")
					await message.reply(embed=em, private=True)
					await message.delete()
				else:
					try:
						channel = await guild.fetch_channel(server["logs_channel_id"])
						em = guilded.Embed(title="A blacklisted word was used.", description="**User** {}\n**ID:** {}\n\n__**READ AT YOUR OWN RISK**__\n`Captures:`\n{}\n\n`Message content:`\n{}".format(author.name, author.id, " \n".join(captures), message.content), color=0x363942)
						await channel.send(embed=em)
						em = guilded.Embed(title="A blacklisted word was used.", description="<@{}> **said:**\n{}".format(author.id, " \n".join(things_said)), color=0x363942)
						em.set_footer(text="Details sent to the logs channel.")
						await message.reply(embed=em, private=True)
						await message.delete()
					except:
						em = guilded.Embed(title="A blacklisted word was used.", description="<@{}> **said:**\n{}".format(author.id, " \n".join(things_said)), color=0x363942)
						em.set_footer(icon_url= "https://img.guildedcdn.com/WebhookThumbnail/aa4b19b0bf393ca43b2f123c22deb94e-Full.webp?w=160&h=160", text="The channel ID set doesn't exist. You may have to set a different ID.")
						await message.reply(embed=em, private=True)
						await message.delete()

	@commands.Cog.listener()
	async def on_message_update(self, event: guilded.MessageUpdateEvent):
		guild = event.server
		author = event.before.author
		before = event.before
		after = event.after
		if before.created_by_bot:
			return

		server = await getServer(guild.id)
		if server["logs_channel_id"] is not None:
			try:
				channel = await guild.fetch_channel(server["logs_channel_id"])
				em = guilded.Embed(title="Message edit event.", description="**User:** {}\n**ID:** {}\n\n__**EDIT EVENT**__\n`Before:`\n{}\n\n`After:`\n{}".format(author.name, author.id, before.content, after.content), color=0x363942)
				await channel.send(embed=em)
			except:
				pass
		else:
			pass

	@commands.Cog.listener()
	async def on_message_delete(self, event: guilded.MessageDeleteEvent):
		guild = event.server
		author = event.message.author
		channel = event.channel
		message = event.message
		if message.created_by_bot:
			return

		server = await getServer(guild.id)
		if server["logs_channel_id"] is not None:
			try:
				channel = await guild.fetch_channel(server["logs_channel_id"])
				em = guilded.Embed(title="Message delete event.", description="**User:** {}\n**ID:** {}\n\n__**DELETE EVENT**__\n**Deleted message:** {}".format(author.name, author.id, message.content), color=0x363942)
				await channel.send(embed=em)
			except:
				pass
		else:
			pass

async def _check_tokens(author):
	try:
		user = await getUser(author.id)
		with db_connection.connection() as conn:
			cursor = conn.cursor()
			if user["tokens"] == None or user["tokens"] == {}:
				new_account = {
					"tokens": {}
				}
				infoJson = json.dumps(new_account)
				cursor = conn.cursor()
				cursor.execute(f"UPDATE users SET tokens = %s WHERE ID = '{author.id}'",  [infoJson])
				conn.commit()
	except psycopg.DatabaseError as e:
		print(f'Error {e}')

async def _check_inventory(author):
	try:
		item_list = fileIO("economy/items.json", "load")
		user = await getUser(author.id)
		with db_connection.connection() as conn:
			cursor = conn.cursor()
			if user["inventory"] == None or user["inventory"] == {}:
				new_account = {
					"inventory": {
						"items": {},
						"consumables": {}
					}
				}
				infoJson = json.dumps(new_account)
				cursor = conn.cursor()
				cursor.execute(f"UPDATE users SET inventory = %s WHERE ID = '{author.id}'",  [infoJson])
				conn.commit()
			else:
				info = user["inventory"]
				for i in item_list["items"]:
					if not i in info["inventory"]["items"]:
						info["inventory"]["items"][i] = {
							"amount": 0
						}
				infoJson = json.dumps(info)
				cursor.execute(f"UPDATE users SET inventory = %s WHERE ID = '{author.id}'",  [infoJson])
				conn.commit()
	except psycopg.DatabaseError as e:
		print(f'Error {e}')

async def _check_cooldowns_author(author):
	try:
		user = await getUser(author.id)
		with db_connection.connection() as conn:
			cursor = conn.cursor()
			if user["cooldowns"] == None:
				new_account = {
					"dig_timeout": 0,
					"weekly_timeout": 0,
					"rob_timeout": 0,
					"work_timeout": 0,
					"slots_timeout": 0
				}
				infoJson = json.dumps(new_account)
				cursor.execute(f"UPDATE users SET cooldowns = %s WHERE ID = '{author.id}'",  [infoJson])
				conn.commit()
	except psycopg.DatabaseError as e:
		print(f'Error {e}')
		

async def _check_inventory_member(member):
	try:
		item_list = fileIO("economy/items.json", "load")
		user = await getUser(member.id)
		with db_connection.connection() as conn:
			cursor = conn.cursor()
			if user["inventory"] == None:
				new_account = {
					"inventory": {
						"items": {},
						"consumables": {}
					}
				}
				infoJson = json.dumps(new_account)
				cursor.execute(f"UPDATE users SET inventory = %s WHERE ID = '{member.id}'",  [infoJson])
				conn.commit()
			else:
				info = user["inventory"]
				for i in item_list["items"]:
					if not i in info["inventory"]["items"]:
						info["inventory"]["items"][i] = {
							"amount": 0
						}
				infoJson = json.dumps(info)
				cursor.execute(f"UPDATE users SET inventory = %s WHERE ID = '{member.id}'",  [infoJson])
				conn.commit()
	except psycopg.DatabaseError as e:
		print(f'Error {e}')

async def _check_values_member(member):
	try:
		new_account = {
			"dig_timeout": 0,
			"weekly_timeout": 0,
			"rob_timeout": 0,
			"work_timeout": 0,
			"slots_timeout": 0
		}
		infoJson = json.dumps(new_account)
		user = await getUser(member.id)
		with db_connection.connection() as conn:
			if user == None:
				cursor = conn.cursor()
				cursor.execute(f"INSERT INTO users(id, bank, bank_access_code, bank_secure, pocket, commands_used) VALUES('{member.id}', 500, '{str(uuid.uuid4().hex)}', 'False', 0, 0)")
				conn.commit()
			await _check_inventory_member(member)

	except psycopg.DatabaseError as e:
		print(f'Error {e}')

async def check_leaderboard(author):
	try:
		user = await getUser(author.id)
		with db_connection.connection() as conn:
			if not user == None:
				lb_user = await getUserLB(author.id)
				if lb_user == None:
					cursor = conn.cursor()
					cursor.execute(f"INSERT INTO leaderboard(id, name, currency) VALUES('{author.id}', 'None', 0)")
					conn.commit()
			await _check_inventory(author)
	except psycopg.DatabaseError as e:
		print(f'Error {e}')

async def command_processed(message, author):
	try:
		user = await getUser(author.id)
		with db_connection.connection() as conn:
			cursor = conn.cursor()
			total_amount = user["commands_used"] + 1
			cursor.execute(f"UPDATE users SET commands_used = {total_amount} WHERE ID = '{author.id}'")
			conn.commit()
			if total_amount == 5:
				em = guilded.Embed(title="Hello {}!".format(author.name), description="I see that you like using me! Here are some links that may be useful to you!\n\n**Links**\n[Support server](https://guilded.gg/Rayz) • [Invite Rayz](https://www.guilded.gg/b/e249e5b0-cbd9-4318-92bb-9cc7fb8c6778)", color=0x363942)
				em.set_footer(text="This message will only appear once for you.")
				await message.reply(embed=em, private=True)
	except psycopg.DatabaseError as e:
		print(f'Error {e}')


async def check_leaderboard_author(author):
	try:
		user = await getUser(author.id)
		with db_connection.connection() as conn:
			cursor = conn.cursor()
			new_LB_bal = user["bank"] + user["pocket"]
			cursor.execute(f"UPDATE leaderboard SET currency = {new_LB_bal} WHERE ID = '{author.id}'")
			cursor.execute(f"UPDATE leaderboard SET name = '{author.name}' WHERE ID = '{author.id}'")
			conn.commit()
	except psycopg.DatabaseError as e:
		print(f'Error {e}')

async def _check_values(author):
	try:
		new_account = {
			"dig_timeout": 0,
			"weekly_timeout": 0,
			"rob_timeout": 0,
			"work_timeout": 0,
			"slots_timeout": 0
		}
		infoJson = json.dumps(new_account)
		user = await getUser(author.id)
		with db_connection.connection() as conn:
			if user == None:
				cursor = conn.cursor()
				cursor.execute(f"INSERT INTO users(id, bank, bank_access_code, bank_secure, pocket, commands_used) VALUES('{author.id}', 500, '{str(uuid.uuid4().hex)}', 'False', 0, 0)")
				conn.commit()
			await _check_tokens(author)
			await _check_inventory(author)
			await _check_cooldowns_author(author)
	except psycopg.DatabaseError as e:
		print(f'Error {e}')

async def _check_values_guild(guild):
	try:
		server = await getServer(guild.id)
		with db_connection.connection() as conn:
			if server == None:
				cursor = conn.cursor()
				cursor.execute(f"INSERT INTO servers(id, logs_channel_id, server_prefix, partner_status, economy_multiplier, moderation_module, fun_module, economy_module) VALUES('{guild.id}', 'None', '?', 'False', 1, 'Enabled', 'Enabled', 'Enabled')")
				conn.commit()
	except psycopg.DatabaseError as e:
		print(f'Error {e}')


def setup(bot):
	bot.add_cog(Generator(bot))
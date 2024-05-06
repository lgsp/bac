from manim import *
import manim
from math import e, pi
import math
from PIL import Image

def disp_sub(self, lang):
    if lang.lower() == "en":
        written, phon = "Subscribe", "/səbˈskraɪb/"
        sub_pic = SVGMobject("/Users/dn/Documents/pics/svg/subscribe.svg")
        sub_scale = 0.8 
    elif lang.lower() == "fr":
        written, phon = "Abonnez-vous", "/abɔne vu/"
        sub_pic = ImageMobject("/Users/dn/Documents/pics/png/sabonner.png")
        sub_scale = 0.45
    elif lang.lower() == "ru":
        written, phon = "Подпишитесь", "/pɐd'piʂitʲɪsʲ/"

    sub = Paragraph(written, phon, line_spacing=0.5)
    self.play(GrowFromCenter(sub))
    self.wait(.5)
    self.play(FadeOut(sub))
    self.add(sub_pic.scale(sub_scale))
    self.wait(.5)

    
def disp_full_part_full(self, full, part, images, lang, full_scale=1):
    self.play(Write(full.scale(full_scale), run_time = 5))
    self.wait(.5)
    self.play(FadeOut(full))

    for img in images:
        pic = ImageMobject(img)
        self.add(pic.scale(0.25))
        self.wait(.5)
        self.remove(pic)
        
    self.play(Write(part.scale(full_scale), run_time = 3))
    self.wait(.5)
        
    self.play(ReplacementTransform(part, full), run_time=3)
    self.wait(.5)
    self.play(FadeOut(full))
    
    disp_sub(self, lang)


    
def inbox_msg(*inboxes, font_size):
    msg_text = ""
    for inbox in inboxes:
        msg_text += r"\mbox{" + f"{inbox}" + r"} \\"
    msg = MathTex(
        msg_text,
        tex_template=TexFontTemplates.french_cursive,
        font_size=font_size
    )
    return msg



def get_regular_polygon(n_gon):
    angle = (360 / n_gon) * DEGREES
    poly_n_gon = RegularPolygon(
        n = n_gon,
        start_angle = angle,
        color = RED
    )
    return poly_n_gon    



def replace_and_write(self, old, new, pos_ref, duration, **lines_and_scales):
    to_be_continued = False
    m, n = len(old), len(new)
    min_mn = m
    keys = lines_and_scales.keys()
    
    if m < n:
        to_be_continued = True
        min_mn = m
    elif m > n:
        self.play(*[FadeOut(old[i]) for i in range(n, m)])
        to_be_continued = False
        min_mn = n
    else: min_mn = m
    
    if lines_and_scales == {}:
        self.play(
            ReplacementTransform(
                old[0], new[0].next_to(pos_ref, 3 * DOWN)
            ),
            *[
                ReplacementTransform(
                    old[i],
                    new[i].next_to(new[i-1], DOWN)
                ) for i in range(1, min_mn)
            ]
        )
        if to_be_continued:
            self.play(
                *[
                    Write(new[i].next_to(new[i-1], DOWN)
                          ) for i in range(min_mn, n)
                ]
            )
    else:
        self.play(
            *[
                ReplacementTransform(
                old[0],
                new[0].scale(
                    lines_and_scales['0']
                ).next_to(pos_ref, 3 * DOWN)
                ) for i in range(1) if '0' in keys
              ],
            *[
                ReplacementTransform(
                old[0],
                new[0].next_to(pos_ref, 3 * DOWN)
                ) for i in range(1) if '0' not in keys
              ],
            *[
                ReplacementTransform(
                    old[i],
                    new[i].scale(
                        lines_and_scales[str(i)]
                    ).next_to(new[i - 1], DOWN)
                ) for i in range(1, min_mn) if str(i) in keys
            ],
            *[
                ReplacementTransform(
                    old[i],
                    new[i].next_to(new[i-1], DOWN)
                ) for i in range(1, min_mn) if str(i) not in keys
            ],
        )
        if to_be_continued:
            self.play(
                *[
                    Write(
                        new[i].scale(
                            lines_and_scales[str(i)]).next_to(
                                new[i - 1], DOWN)
                    ) for i in range(min_mn, n) if str(i) in keys
                ],
                *[
                    Write(
                        new[i].next_to(new[i - 1], DOWN)
                    ) for i in range(min_mn, n) if not str(i) in keys
                ],
            )
    
    self.wait(duration)


    
    
def cursive_msg(phrase, sep, font_size=40):
    inboxes = phrase.split(sep)
    msg = inbox_msg(*inboxes, font_size=font_size)
    return msg



def targets_to_write(text, ref, size=1, direction=DOWN):
    #text = [Text(t) for t in text if isinstance(t, str)]
    n = len(text)
    # Create a list of target objects
    targets = [text[0].next_to(ref, size * direction)]
    targets += [
        text[i].next_to(
            text[i - 1],
            size * direction
        ) for i in range(1, n)
    ]
    return text


##################################################
# Aix-Marseille 1981 Exo 1
##################################################

# Exo 1
class AixMars1981Exo1Question1(Scene):
    def construct(self):
        msg1 = "Bac Aix-Marseille 1981"
        title1 = Title(f"{msg1}")
        self.add(title1.scale(1))
        self.wait(2)

        but0 = r"\textsc{EXERCICE} 1"
        but1 = r"Le but de cet exercice est de démontrer par l'absurde "
        but2 = r"qu'il existe une infinité de nombres premiers de la "
        but3 = r"forme \(4n - 1\), où \(n\) est un élément de "
        but3 += r"\(\mathbb{N}^{*}\)"
        but4 = r"(ensemble des entiers naturels non nuls)"
        buts = [Tex(b) for b in [but0, but1, but2, but3, but4]]
        for i in range(len(buts)):
            self.play(Write(buts[i].next_to(title1, (2 + 4 * i) * DOWN)))
            self.wait(1.25)

        
        question1 = Title("Question 1")
        self.play(
            ReplacementTransform(title1, question1),
            FadeOut(*buts)
        )
        self.wait(2)
        

        q10 = r"Soit \(E\) l'ensemble des nombres premiers de la forme "
        q11 = r"\(4n - 1\), où \(n\) est un élément de \(\mathbb{N}^{*}\)."
        q12 = r"Montrer que \(E\) a au moins deux éléments."
        q1 = [Tex(q) for q in [q10, q11, q12]]
        for i in range(len(q1)):
            self.play(Write(q1[i].next_to(title1, (2 + 4 * i) * DOWN)))
            self.wait(1.25)

        
        rep1 = Title("Réponse à la question 1")
        self.play(
            ReplacementTransform(question1, rep1),
        )
        self.wait(2)

        r10 = r"Prenons \(n = 1\) et on obtient \(e_1 = 3\in E\)."
        r11 = r"Prenons \(n = 2\) et on obtient \(e_2 = 7\in E\)."
        r12 = r"Ainsi \(\{e_1 = 3, e_2 = 7\}\in E\) et "
        r12 += r"\(Card(E)\geqslant 2\)."
        r1 = [Tex(r) for r in [r10, r11, r12]]
        for i in range(len(r1)):
            self.play(Write(r1[i].next_to(q1[-1], (2 + 4 * i) * DOWN)))
            self.wait(1.25)


        question2 = Title("Question 2")
        self.play(
            ReplacementTransform(rep1, question2),
            FadeOut(*q1),
            FadeOut(*r1)
        )
        self.wait(2)

        q20 = r"\textit{On suppose} \(E\) \textit{fini}. "
        q20 += r"Soit \(P\) le produit"
        q21 = r"de tous les éléments de \(E\) et \(X = 4P - 1\)."
        q2 = [Tex(q) for q in [q20, q21]]
        for i in range(len(q2)):
            self.play(Write(q2[i].next_to(question2, (2 + 4 * i) * DOWN)))
            self.wait(1.25)


        question2a = Title("Question 2.a")
        q2a = Tex(r"a. Trouver un minorant de \(X\).")
        self.play(
            ReplacementTransform(question2, question2a),
            Write(q2a.next_to(q2[-1], 2 * DOWN))
        )
        self.wait(2)

        rep2a = Title("Réponse à la question 2.a")
        self.play(
            ReplacementTransform(question2a, rep2a),
            FadeOut(*q2),
            FadeOut(*q2a)
        )
        self.wait(2)
        
        # r2a0 = r"Commençons par poser \(E = \{e_1, \dots , e_n\}\)."
        # r2a1 = r"Ensuite "
        # r2a1 += r"\(P = \prod_{i = 1}^ne_i\) "
        # r2a1 += r"i.e \(P = e_1\times e_2\times\dots \times e_n\)."
        # r2a2 = r"Il vient \(X = 4\prod_{i = 1}^ne_i - 1\)."
        
        r2a0 = r"D'après la question 1, \(Card(E) \geqslant 2\)."
        r2a1 = r"Par construction \(e_1 = 3\) et \(e_2 = 7\) sont"
        r2a2 = r"les plus petits éléments de \(E\)."
        r2a3 = r"Ainsi \(P\) est minoré, \(P\geqslant 21 ( = 3\times 7)\)."
        r2a4 = r"Par suite, \(X\geqslant 83 ( = 4\times 21 - 1)\)."

        r2a = [
            Tex(r) for r in [
                r2a0, r2a1, r2a2, r2a3, r2a4
            ]
        ]
        for i in range(len(r2a)):
            self.play(
                Write(r2a[i].next_to(
                    rep2a,
                    (2 + 4 * i) * DOWN
                )
                    )
            )
            self.wait(1.25)

        
        question2b = Title("Question 2.b")
        q2b0 = r"Montrer que \(X\) n'est pas divisible par 2, "
        q2b1 = r"et en déduire que tout facteur premier de \(X\) est"
        q2b2 = r"soit de la forme \(4n + 1\), soit de la forme \(4n - 1\)"
        q2b3 = r"où \(n\) est un élément de \(\mathbb{N}^{*}\)."
        q2b = [Tex(q) for q in [q2b0, q2b1, q2b2, q2b3]]
        
        self.play(
            ReplacementTransform(rep2a, question2b),
            FadeOut(*r2a)
        )
        self.wait(2)

        for i in range(len(q2b)):
            self.play(
                Write(
                    q2b[i].next_to(
                        question2b,
                        (2 + 4 * i) * DOWN
                    )
                )
            )
            self.wait(1.25)

        rep2b = Title("Réponse à la question 2.b")
        self.play(
            ReplacementTransform(question2b, rep2b),
            FadeOut(*q2b),
        )
        self.wait(2)

        r2b0 = r"Reformulons, \(X = 4P - 1 = 2(2P) - 1\)"
        r2b1 = r"\(X\) est par construction impair."
        r2b2 = r"Donc ses facteurs premiers le sont aussi."
        r2b3 = r"Tout nombre entier impair s'écrit soit \(4n + 1\)"
        r2b4 = r"soit \(4n + 3\) or modulo 4, \(4n + 3 = 4n - 1\)."
        r2b5 = r"Vous pouvez vérifier que \(4n\) et \(4n + 2\) sont pairs."
        r2b = [
            Tex(r) for r in [
                r2b0, r2b1, r2b2, r2b3, r2b4, r2b5
            ]
        ]
        for i in range(len(r2b)):
            self.play(
                Write(r2b[i].next_to(
                    rep2b,
                    (2 + 4 * i) * DOWN
                )
                    )
            )
            self.wait(1.25)

        question2c = Title("Question 2.c")
        self.play(
            ReplacementTransform(rep2b, question2c),
            FadeOut(*r2b)
        )
        self.wait(2)

        
        q2c0 = r"Montrer que \(X\) possède au moins un facteur premier "
        q2c1 = r"de la forme \(4n - 1\) où \(n\) est un élément de "
        q2c1 += r"\(\mathbb{N}^{*}\)."
        q2c = [Tex(q) for q in [q2c0, q2c1]]
        for i in range(len(q2c)):
            self.play(
                Write(
                    q2c[i].next_to(
                        question2c,
                        (2 + 4 * i) * DOWN
                    )
                )
            )
            self.wait(1.25)


        rep2c = Title("Réponse à la question 2.c")
        self.play(
            ReplacementTransform(question2c, rep2c),
        )
        self.wait(2)
        
        r2c0 = r"Supposons par l'absurde que \(X\) ne possède pas de "
        r2c1 = r"facteur premier de la forme \(4n - 1\)."
        r2c2 = r"D'après 2.b, alors tous ses facteurs premiers seraient"
        r2c3 = r"de la forme \(4n + 1\). Or modulo 4, \(4n + 1\equiv 1\)."
        r2c4 = r"Ainsi, cela impliquerait que \(X \equiv 1 [4]\)."
        r2c5 = r"Ce qui contredit sa définition "
        r2c5 += r"\(X = 4P - 1\equiv -1 [4]\)."
        r2c = [
            Tex(r) for r in [
                r2c0, r2c1, r2c2, r2c3, r2c4, r2c5
            ]
        ]
        for i in range(len(r2c)):
            self.play(
                Write(r2c[i].next_to(
                    q2c[-1],
                    (2 + 3 * i) * DOWN
                )
                    )
            )
            self.wait(1.25)

        question3 = Title("Question 3")
        self.play(
            ReplacementTransform(rep2c, question3),
            FadeOut(*q2c),
            FadeOut(*r2c)
        )
        self.wait(2)

        q30 = r"En considérant un facteur premier \(p\) de \(X\) "
        q30 += r"de la forme \(4n - 1\), "
        q31 = r"la définition de \(P\) et la relation \(X = 4P - 1\), "
        q32 = r"achever la démonstration par l'absurde."
        q3 = [Tex(q) for q in [q30, q31, q32]]
        for i in range(len(q3)):
            self.play(
                Write(q3[i].next_to(question3, (2 + 3 * i) * DOWN))
            )
            self.wait(1.25)

        
        
        
        rep3 = Title("Réponse à la question 3")
        self.play(
            ReplacementTransform(question3, rep3),
        )
        self.wait(2)
        
        r30 = r"D'après 2.c, il existe \(p = 4n - 1\) facteur premier "
        r30 += r"de \(X\). "
        r31 = r"Donc \(p\in E\) or \(E\) étant fini alors "
        r31 += r"\(p\) divise \(P\). "
        r32 = r"Mais si \(p\) divise \(X\) et \(P\) alors \(p\) divise 1 "
        r33 = r"Ce qui est absurde donc \(E\) est nécessairement infini."
        r3 = [
            Tex(r) for r in [
                r30, r31, r32, r33
            ]
        ]
        for i in range(len(r3)):
            self.play(
                Write(r3[i].next_to(
                    q3[-1],
                    (2 + 3 * i) * DOWN
                )
                    )
            )
            self.wait(1.25)

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


############################################################
# Polynésie 2023
############################################################

# Exo 3 Affirmation 1
class PolyExo3Affirmation1(Scene):
    def construct(self):
        msg1 = "Bac 2023 Polynésie exo 3"
        title1 = Title(f"{msg1}")
        self.add(title1.scale(1))
        self.wait(2)
        
        affirmation1 = Title("Affirmation 1")
        self.play(
            ReplacementTransform(title1, affirmation1)
        )
        self.wait()
        

        txt_part0 = r"Pour chacune des affirmations suivantes, "
        part0 = Tex(txt_part0).next_to(affirmation1, DOWN)
        
        txt_part1 = r"indiquer si elle est vraie ou fausse. "
        part1 = Tex(txt_part1).next_to(part0, DOWN)
        
        txt_part2 = r"Chaque réponse doit être justifiée."
        part2 = Tex(txt_part2).next_to(part1, DOWN)

        txt_part3 = r"Une réponse non justifiée ne rapporte aucun point."
        part3 = Tex(txt_part3).next_to(part2, DOWN)

        m_parts = VGroup(part0, part1, part2, part3)
        
        aff1_1 = Tex("Affirmation 1 : ").next_to(part3, 2 * DOWN)
        aff1_2 = Tex(
            r"La fonction \(f\) définie sur \(\mathbb{R}\) par "
        ).next_to(aff1_1, DOWN)
        aff1_3 = Tex(
            r"\(f(x) = e^x - x\) est convexe."
        ).next_to(aff1_2, DOWN)
        m_affs = VGroup(aff1_1, aff1_2, aff1_3)
        
        mobj1 = VGroup(m_parts, m_affs)


        self.play(
            Write(mobj1.next_to(affirmation1, 2 * DOWN))
        )
        self.wait(4)

        noter = Title("Mettez pause pour noter la affirmation")
        self.play(
            ReplacementTransform(affirmation1, noter)
        )
        self.wait(4)

        attention_rep = Title("Cherchez avant de regarder le corrigé")
        self.play(
            ReplacementTransform(noter, attention_rep)
        )
        self.wait(4)
        
        solution1 = Title("Affirmation vraie.")

        r10 = r"f(x) = e^x - x"
        r11 = r"f'(x) = e^x - 1"
        r12 = r"f''(x) = e^x > 0"
        
        rep = [r10, r11, r12]
        p = [MathTex(r) for r in rep]
        
        self.play(
            ReplacementTransform(attention_rep, solution1),
            ReplacementTransform(
                mobj1,
                p[0].next_to(affirmation1, 2 * DOWN)
            )
        )
        self.wait()

        self.play(
            *[
                Write(
                    p[i].next_to(p[i-1], 3 * DOWN)
                ) for i in range(1, len(p))
            ]
        )
        self.wait(5)

        

        box_res = SurroundingRectangle(p[-1])
        self.play(
            Write(box_res)
        )
        self.wait(2)

        
        

# Exo 3 Affirmation 2
class PolyExo3Affirmation2(Scene):
    def construct(self):
        msg1 = "Bac 2023 Polynésie exo 3"
        title1 = Title(f"{msg1}")
        self.add(title1.scale(1))
        self.wait(2)
        
        affirmation2 = Title("Affirmation 2")
        self.play(
            ReplacementTransform(title1, affirmation2)
        )
        self.wait()
        

        txt_part0 = r"Pour chacune des affirmations suivantes, "
        part0 = Tex(txt_part0).next_to(affirmation2, DOWN)
        
        txt_part1 = r"indiquer si elle est vraie ou fausse. "
        part1 = Tex(txt_part1).next_to(part0, DOWN)
        
        txt_part2 = r"Chaque réponse doit être justifiée."
        part2 = Tex(txt_part2).next_to(part1, DOWN)

        txt_part3 = r"Une réponse non justifiée ne rapporte aucun point."
        part3 = Tex(txt_part3).next_to(part2, DOWN)

        m_parts = VGroup(part0, part1, part2, part3)
        
        aff2_1 = Tex("Affirmation 2 : ").next_to(part3, 2 * DOWN)
        aff2_2 = Tex(
            r"L'équation \((2e^x - 6)(e^x + 2) = 0\) admet "
        ).next_to(aff2_1, DOWN)
        aff2_3 = Tex(
            r"\(\ln(3)\) comme unique solution dans \(\mathbb{R}\)."
        ).next_to(aff2_2, DOWN)
        m_affs = VGroup(aff2_1, aff2_2, aff2_3)
        
        mobj1 = VGroup(m_parts, m_affs)


        self.play(
            Write(mobj1.next_to(affirmation2, 2 * DOWN))
        )
        self.wait(4)

        noter = Title("Mettez pause pour noter la affirmation")
        self.play(
            ReplacementTransform(affirmation2, noter)
        )
        self.wait(4)

        attention_rep = Title("Cherchez avant de regarder le corrigé")
        self.play(
            ReplacementTransform(noter, attention_rep)
        )
        self.wait(4)
        
        solution1 = Title("Affirmation vraie.")

        r10 = r"(2e^x - 6)(e^x + 2) = 0"
        r11 = r"e^x + 2 > 2\Rightarrow 2e^x - 6 = 0"
        r12 = r"2e^x - 6 = 0\Rightarrow 2e^x = 6"
        r13 = r"2e^x = 6\Rightarrow e^x = \dfrac{6}{2}"
        r14 = r"e^x = \dfrac{6}{2}\Rightarrow e^x = 3"
        r15 = r"e^x = 3\Rightarrow x = \ln(3)"
        r16 = r"x = \ln(3)"
        
        rep = [r10, r11, r12, r13, r14, r15, r16]
        p = [MathTex(r) for r in rep]
        
        self.play(
            ReplacementTransform(attention_rep, solution1),
            ReplacementTransform(
                mobj1,
                p[0].next_to(affirmation2, 2 * DOWN)
            )
        )
        self.wait()

        self.play(
            *[
                Write(
                    p[i].next_to(p[i-1], 3 * DOWN)
                ) for i in range(1, len(p) // 2 + 1)
            ]
        )
        self.wait(5)

        self.play(
            *[
                ReplacementTransform(
                    p[i],
                    p[i + len(p) // 2].next_to(p[i], 3 * DOWN)
                ) for i in range(len(p) // 2)
            ]
        )
        self.wait(5)

        

        box_res = SurroundingRectangle(p[-1])
        self.play(
            *[FadeOut(p[i]) for i in range(len(p) - 1)]
        )
        self.wait(2)

        m_final = VGroup(p[-1], box_res)

        self.play(
            m_final.animate.next_to(affirmation2, 2 * DOWN)
        )
        self.wait(2)

        
        
        

# Exo 3 Affirmation 3
class PolyExo3Affirmation3(Scene):
    def construct(self):
        msg1 = "Bac 2023 Polynésie exo 3"
        title1 = Title(f"{msg1}")
        self.add(title1.scale(1))
        self.wait(2)
        
        affirmation3 = Title("Affirmation 3")
        self.play(
            ReplacementTransform(title1, affirmation3)
        )
        self.wait()
        

        txt_part0 = r"Pour chacune des affirmations suivantes, "
        part0 = Tex(txt_part0).next_to(affirmation3, DOWN)
        
        txt_part1 = r"indiquer si elle est vraie ou fausse. "
        part1 = Tex(txt_part1).next_to(part0, DOWN)
        
        txt_part2 = r"Chaque réponse doit être justifiée."
        part2 = Tex(txt_part2).next_to(part1, DOWN)

        txt_part3 = r"Une réponse non justifiée ne rapporte aucun point."
        part3 = Tex(txt_part3).next_to(part2, DOWN)

        m_parts = VGroup(part0, part1, part2, part3)
        
        aff3_1 = Tex("Affirmation 3 : ").next_to(part3, 2 * DOWN)
        aff3_2 = Tex(
            r"\[\lim_{x\to +\infty} \dfrac{e^{2x} - 1}{e^x - x} = 0\]"
        ).next_to(aff3_1, DOWN)

        m_affs = VGroup(aff3_1, aff3_2)
        
        mobj1 = VGroup(m_parts, m_affs)


        self.play(
            Write(mobj1.next_to(affirmation3, 2 * DOWN))
        )
        self.wait(4)

        noter = Title("Mettez pause pour noter la affirmation")
        self.play(
            ReplacementTransform(affirmation3, noter)
        )
        self.wait(4)

        attention_rep = Title("Cherchez avant de regarder le corrigé")
        self.play(
            ReplacementTransform(noter, attention_rep)
        )
        self.wait(4)
        
        solution1 = Title("Affirmation fausse.")

        r10 = r"\dfrac{e^{2x} - 1}{e^x - x} = "
        r10 += r"\dfrac{e^{2x}\left(1 - \frac{1}{e^{2x}}\right)}"
        r10 += r"{e^{2x}\left(\frac{e^x}{e^{2x}} - \frac{x}{e^{2x}}\right)}"
        r11 = r"\dfrac{e^{2x} - 1}{e^x - x} = "
        r11 += r"\dfrac{1 - \frac{1}{e^{2x}}}"
        r11 += r"{\frac{e^x}{e^{2x}} - \frac{x}{e^{2x}}}"
        
        r12 = r"\dfrac{e^{2x} - 1}{e^x - x} = "
        r12 += r"\dfrac{1 - \frac{1}{(e^{x})^2}}"
        r12 += r"{\frac{1}{e^{x}} - \frac{x}{(e^{x})^2}}"
        
        r13 = r"\lim_{x\to +\infty}e^{-x} = "
        r13 += r"\lim_{x\to +\infty}\frac{1}{e^{x}} = 0"
        r13 += r"\Rightarrow \lim_{x\to +\infty}e^{-2x} = 0"
        
        r14 = r"e^{2x} = (e^x)^2\Rightarrow xe^{-2x}} = "
        r14 += r"\dfrac{x}{(e^x)^2} = \frac{x}{e^x}\times\frac{1}{e^x}"
        
        r15 = r"\lim_{x\to +\infty}\dfrac{x}{e^{x}} = 0"
        r15 += r"\Rightarrow \lim_{x\to +\infty}\dfrac{x}{(e^{x})^2} = 0"
        
        r16 = r"\lim_{x\to 0}\dfrac{1}{x} = +\infty"
        r17 = r"\lim_{x\to +\infty}\dfrac{e^{2x} - 1}{e^x - x} = "
        r17 += r"+\infty"
        
        rep = [r10, r11, r12, r13, r14, r15, r16, r17]
        p = [MathTex(r) for r in rep]

        third = len(p) // 3

        
        self.play(
            ReplacementTransform(attention_rep, solution1),
            ReplacementTransform(
                mobj1,
                p[0].next_to(affirmation3, 2 * DOWN)
            )
        )
        self.wait(2)

        for i in range(1, 1 + 2):
            self.play(
                Write(p[i].next_to(p[i - 1], 2 * DOWN))
            )
            self.wait()
        
        for i in range(1, 1 + 2):
            self.play(
                ReplacementTransform(
                    p[i],
                    p[i + 3].next_to(p[i - 1], 2 * DOWN)
                )
            )
            self.wait()

        for i in range(1, 2):
            self.play(
                ReplacementTransform(
                    p[i + 3],
                    p[i + 6].next_to(p[i - 1], 2 * DOWN)
                )
            )
            self.wait()

        

        # self.play(
        #     ReplacementTransform(
        #         m_p1,
        #         m_p2.next_to(affirmation3, 2 * DOWN)
        #     )
        # )
        # self.wait(5)

        # self.play(
        #     ReplacementTransform(
        #         m_p2,
        #         m_p3.next_to(affirmation3, 2 * DOWN)
        #     )
        # )
        # self.wait(5)
        
        box_res = SurroundingRectangle(p[-1])
        self.play(
            *[FadeOut(p[i]) for i in range(len(p) - 1)]
        )
        self.wait(2)

        m_final = VGroup(p[-1], box_res)

        self.play(
            m_final.animate.next_to(affirmation3, 2 * DOWN)
        )
        self.wait(2)

        
        
        
        
# Exo 3 Affirmation 4
class PolyExo3Affirmation4(Scene):
    def construct(self):
        msg1 = "Bac 2023 Polynésie exo 3"
        title1 = Title(f"{msg1}")
        self.add(title1.scale(1))
        self.wait(2)
        
        affirmation4 = Title("Affirmation 4")
        self.play(
            ReplacementTransform(title1, affirmation4)
        )
        self.wait()
        

        txt_part0 = r"Pour chacune des affirmations suivantes, "
        part0 = Tex(txt_part0).next_to(affirmation4, 2 * DOWN)
        
        txt_part1 = r"indiquer si elle est vraie ou fausse. "
        part1 = Tex(txt_part1).next_to(part0, DOWN)
        
        txt_part2 = r"Chaque réponse doit être justifiée."
        part2 = Tex(txt_part2).next_to(part1, DOWN)

        txt_part3 = r"Une réponse non justifiée ne rapporte aucun point."
        part3 = Tex(txt_part3).next_to(part2, DOWN)

        txt_part4 = r"Soit \(f\) la fonction définie sur \(\mathbb{R}\) "
        txt_part4 += r"par \(f(x) = (6x + 5)e^{3x}\) "
        part4 = Tex(txt_part4).next_to(part3, DOWN)

        txt_part5 = r"et \(F\) la fonction définie sur \(\mathbb{R}\) "
        txt_part5 += r"par : \(F(x) = (2x + 1)e^{3x} + 4\)."
        part5 = Tex(txt_part5).next_to(part4, DOWN)

        parts = [part0, part1, part2, part3, part4, part5]
        m_parts = VGroup(*parts)

        aff_txt1 = r"Affirmation 4 : "
        aff_txt1 += r"\(F\) est la primitive de \(f\) "
        aff4_1 = Tex(aff_txt1).next_to(part5, 2 * DOWN)

        aff_txt2 = r"sur \(\mathbb{R}\) qui "
        aff_txt2 += r"prend la valeur 5 quand \(x = 0\)."
        aff4_2 = Tex(aff_txt2).next_to(aff4_1, DOWN)

        m_affs = VGroup(aff4_1, aff4_2)
        
        mobj1 = VGroup(m_parts, m_affs)


        self.play(
            Write(mobj1.next_to(affirmation4, 2 * DOWN))
        )
        self.wait(4)

        noter = Title("Mettez pause pour noter la affirmation")
        self.play(
            ReplacementTransform(affirmation4, noter)
        )
        self.wait(4)

        attention_rep = Title("Cherchez avant de regarder le corrigé")
        self.play(
            ReplacementTransform(noter, attention_rep)
        )
        self.wait(4)
        
        solution1 = Title("Affirmation vraie.")

        r10 = r"F(x) = (2x + 1)e^{3x} + 4"
        
        r11 = r"F = ue^v"
        r112 = r"F' = u'e^v + uv'e^v"

        r12 = r"(u = 2x + 1, v = 3x)\Rightarrow (u' = 2, "
        r12 += r"v' = 3)"
    
        r113 = r"F'(x) = 2e^{3x} + 3(2x + 1)e^{3x}"
        
        r114 = r"F'(x) = (6x + 5)e^{3x}"
        
        r13 = r"F' = f"
                
        r14 = r"F(0) = (2\times 0 + 1)\times e^{3\times 0} + 4"

        r142 = r"F(0) = 5"
        
        rep = [r10, r11, r112, r12, r113, r114, r13, r14, r142]
        p = [MathTex(r) for r in rep]

        
        self.play(
            ReplacementTransform(attention_rep, solution1),
            ReplacementTransform(
                mobj1,
                p[0].next_to(affirmation4, 2 * DOWN)
            )
        )
        self.wait(2)

        self.play(
            Write(p[1].next_to(p[0], DOWN))
        )
        self.wait(2)

        self.play(
            ReplacementTransform(p[1], p[2].next_to(p[0], DOWN))
        )
        self.wait(2)

        self.play(
            Write(p[3].next_to(p[2], DOWN))
        )
        self.wait(2)

        self.play(
            ReplacementTransform(p[2], p[4].next_to(p[3], DOWN))
        )
        self.wait(2)

        self.play(
            ReplacementTransform(p[4], p[5].next_to(p[3], DOWN))
        )
        self.wait(2)
        
        self.play(
            Write(p[6].next_to(p[4], DOWN))
        )
        self.wait(2)

        self.play(
            Write(p[7].next_to(p[6], DOWN))
        )
        self.wait(2)

        self.play(
            ReplacementTransform(p[7], p[8].next_to(p[6], DOWN))
        )
        self.wait(2)
        
        box_res = SurroundingRectangle(p[-1])
        self.play(
            *[FadeOut(p[i]) for i in range(len(p))]
        )
        self.wait(2)

        final = MathTex(
            r"F(x) = (2x + 1)e^{3x} + 4"
        ).next_to(affirmation4, 2 * DOWN)
        final2 = MathTex(
            r"F'(x) = f(x) = (6x + 5)e^{3x}"
        ).next_to(final, DOWN)
        final3 = MathTex(
            r"F(0) = 5"
        ).next_to(final2, 2 * DOWN)
        finals = VGroup(final, final2, final3)
        b_final = SurroundingRectangle(finals)
        mobj_final = VGroup(finals, b_final)

        self.play(
            mobj_final.animate.next_to(affirmation4, 2 * DOWN)
        )
        self.wait(2)

        
        
        
        
# Exo 3 Affirmation 5
class PolyExo3Affirmation5(Scene):
    def construct(self):
        msg1 = "Bac 2023 Polynésie exo 3"
        title1 = Title(f"{msg1}")
        self.add(title1.scale(1))
        self.wait(2)
        
        affirmation5 = Title("Affirmation 5")
        self.play(
            ReplacementTransform(title1, affirmation5)
        )
        self.wait()
        

        txt_part0 = r"Pour chacune des affirmations suivantes, "
        part0 = Tex(txt_part0).next_to(affirmation5, 2 * DOWN)
        
        txt_part1 = r"indiquer si elle est vraie ou fausse. "
        part1 = Tex(txt_part1).next_to(part0, DOWN)
        
        txt_part2 = r"Chaque réponse doit être justifiée."
        part2 = Tex(txt_part2).next_to(part1, DOWN)

        txt_part3 = r"Une réponse non justifiée ne rapporte aucun point."
        part3 = Tex(txt_part3).next_to(part2, DOWN)

        txt_part4 = r"On rappelle que len(L) représente la longueur"
        txt_part4 += r" de la liste L."
        part4 = Tex(txt_part4).next_to(part3, DOWN)

        txt_part5 = """def mystere(L):
    S = 0
    for i in range(len(L)):
        S = S + L[i]
    return S / len(L)
"""        
        part5 = Code(
            code=txt_part5,
            tab_width=4,
            background="window",
            language="Python",
            font="Monospace"
        ).next_to(part4, DOWN)
        

        parts = [part0, part1, part2, part3, part4, part5]
        m_parts = VGroup(*parts)

        aff_txt1 = r"Affirmation 5 : "
        aff5_1 = Tex(aff_txt1).next_to(part5, 2 * DOWN)

        aff_txt2 = r"L'exécution de "
        aff_txt2 += r"mystere([1, 9, 9, 5, 0, 3, 6, 12, 0, 5]) "
        aff_txt2 += r"renvoie 50."

        aff5_2 = Tex(aff_txt2).next_to(aff5_1, DOWN)

        m_affs = VGroup(aff5_1, aff5_2)
        
        mobj1 = VGroup(m_parts, m_affs)


        self.play(
            Write(mobj1.next_to(affirmation5, 2 * DOWN))
        )
        self.wait(4)

        noter = Title("Mettez pause pour noter la affirmation")
        self.play(
            ReplacementTransform(affirmation5, noter)
        )
        self.wait(4)

        attention_rep = Title("Cherchez avant de regarder le corrigé")
        self.play(
            ReplacementTransform(noter, attention_rep)
        )
        self.wait(4)
        
        solution1 = Title("Affirmation fausse.")

        r10 = r"0 + 1 + 9 + 9 + 5 + 0 + 3 + 6 + 12 + 0 + 5 = 50"
        
        r11 = r"50 / 5 = 10"
        
        r12 = r"La fonction mystère calcule la moyenne."

        
        rep = [r10, r11, r12]
        p = [Tex(r) for r in rep]

        
        self.play(
            ReplacementTransform(attention_rep, solution1),
            ReplacementTransform(
                mobj1,
                p[0].next_to(affirmation5, 2 * DOWN)
            )
        )
        self.wait(2)

        self.play(
            Write(p[1].next_to(p[0], DOWN))
        )
        self.wait(2)

        self.play(
            Write(p[2].next_to(p[1], DOWN))
        )
        self.wait(2)

        t0 = IntegerTable(
            [
                [1, 9, 9, 5, 0, 3, 6, 12, 0, 5],
                [
                    0 + 1,
                    1 + 9,
                    10 + 9,
                    19 + 5,
                    24 + 0,
                    24 + 3,
                    27 + 6,
                    33 + 12,
                    45 + 0,
                    45 + 5
                ]
            ],
            col_labels=[
                MathTex(r"0"), MathTex(r"1"),
                MathTex(r"2"), MathTex(r"3"),
                MathTex(r"4"), MathTex(r"5"),
                MathTex(r"6"), MathTex(r"7"),
                MathTex(r"8"), MathTex(r"9"),
            ],
            row_labels=[MathTex("L"), MathTex("S")],
            h_buff=1,
        ).scale(0.85)
        
        final = t0.next_to(p[2], DOWN)
        b_final = SurroundingRectangle(final)
        mobj_final = VGroup(final, b_final)

        self.play(
            mobj_final.animate.next_to(p[2], DOWN)
        )
        self.wait(2)
        
        

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

def disp_calculations(self, previous_mobj, calcs, next2obj, direction):
            """
            This function replace previous_mobj with calcs next2obj
            
            previous_mobj: mobj to replace
            calcs: calculations to display
            next2obj: obj nearby to display
            direction: direction from next2obj
            """
            if previous_mobj:
                self.play(
                    ReplacementTransform(
                        previous_mobj,
                        calcs[0].next_to(next2obj, direction)
                    )
                )
            else:
                self.play(
                    Write(calcs[0].next_to(next2obj, direction))
                )
            self.wait()
            for i in range(len(calcs) - 1):
                self.play(
                    ReplacementTransform(
                        calcs[i],
                        calcs[i+1].next_to(next2obj, direction)
                    )
                )
                self.wait()

def disp_tex_list(self, previous_mobj, tex_list, next2obj, direction):
            """
            This function replace previous_mobj with tex_list next2obj
            
            previous_mobj: mobj to replace
            tex_list: list with Tex mobjs to display
            next2obj: obj nearby to display
            direction: direction from next2obj
            """
            if previous_mobj:
                self.play(
                    ReplacementTransform(
                        previous_mobj,
                        tex_list[0].next_to(next2obj, direction)
                    )
                )
            else:
                self.play(
                    Write(tex_list[0].next_to(next2obj, direction))
                )
            self.wait()
            for i in range(len(tex_list) - 1):
                self.play(
                    Write(
                        tex_list[i+1].next_to(tex_list[i], direction)
                    )
                )
                self.wait()
                
##################################################
# USA 27 mars 2023 Sujet 1
##################################################

# Exo 3 Question 1
class USAExo3Question1(Scene):
    def construct(self):
        msg1 = "Bac USA 27 mars 2023 Sujet 1 Exercice 3"
        title1 = Title(f"{msg1}")
        self.add(title1.scale(1))
        self.wait(2)

        intro = [
            r"L'espace est muni d'un repère orthonormé \((O; \vec{\imath}, \vec{\jmath}, \vec{k})\).",
            r"On considère les points \(A(-1;2;5)\), \(B(3; 6; 3)\), \(C(3; 0; 9)\) et \(D(8; -3; -8)\).",
            r"On admet que les points A, B, et C ne sont pas alignés."
        ]

        intro_tex = [Tex(i) for i in intro]
        self.play(
            Write(intro_tex[0].scale(0.75).next_to(title1, DOWN))
        )
        self.wait()
        for i in range(len(intro) - 1):
            self.play(
                Write(intro_tex[i+1].scale(0.75).next_to(intro_tex[i], DOWN))
            )
            self.wait()

        question1 = Title("Question 1")
        q1 = Tex(r"1. ABC est un triangle : ")
        a = r"a. isocèle rectangle en A"
        b = r"b. isocèle rectangle en B"
        c = r"c. isocèle rectangle en C"
        d = r"d. équilatéral"
        m1 = MobjectMatrix(
            [[Tex(a), Tex(b)], [Tex(c), Tex(d)]],
            v_buff=2.5,
            h_buff=8,
            left_bracket="\{",
            right_bracket="\}"
        ).next_to(q1, DOWN)

        mobj1 = VGroup(q1, m1).scale(0.75)
        
        self.play(
            ReplacementTransform(title1, question1),
            Write(mobj1.next_to(intro_tex[-1], DOWN))
        )
        self.wait(4)

        noter = Title("Mettez pause pour noter la question")
        self.play(
            ReplacementTransform(question1, noter)
        )
        self.wait(4)

        attention_rep = Title("Cherchez avant de regarder le corrigé")
        self.play(
            ReplacementTransform(noter, attention_rep)
        )
        self.wait(4)

        ent = m1.get_entries()
        sol_a = ent[0]
        box_a = SurroundingRectangle(sol_a)
        solution1 = Title("Réponse a")
        self.play(
            ReplacementTransform(attention_rep, solution1),
            Write(box_a)
        )
        self.wait()

        
        explanation = Title("Explications")

        self.play(
            Unwrite(box_a),
            ReplacementTransform(solution1, explanation)
        )
        self.wait()
        
        AB00 = r"\(AB^2 = (3 - (-1))^2 + (6 - 2)^2 + (3 - 5)^2\)"
        AB01 = r"\(AB^2 = 4^2 + 4^2 + 4\)"
        AB02 = r"\(AB^2 = 4(4 + 4 + 1)\)"
        AB03 = r"\(AB^2 = 4\times 9\)"
        AB04 = r"\(AB^2 = 6^2\)"
        
        AB = [AB00, AB01, AB02, AB03, AB04]
        dAB = [Tex(d).scale(0.75) for d in AB]

        

        disp_calculations(self, 
            previous_mobj=mobj1,
            calcs=dAB,
            next2obj=intro_tex[-1],
            direction=DOWN
        )
        
        self.play(
            dAB[-1].animate.shift(3 * LEFT)
        )
        self.wait()

        AC00 = r"\(AC^2 = (3 - (-1))^2 + (0 - 2)^2 + (9 - 5)^2\)"
        AC01 = r"\(AC^2 = 4^2 + 4 + 4^2\)"
        AC02 = r"\(AC^2 = 4(4 + 4 + 1)\)"
        AC03 = r"\(AC^2 = 4\times 9\)"
        AC04 = r"\(AC^2 = 6^2\)"
        
        AC = [AC00, AC01, AC02, AC03, AC04]
        dAC = [Tex(d).scale(0.75) for d in AC]

        disp_calculations(self, 
            previous_mobj=None,
            calcs=dAC,
            next2obj=dAB[-1],
            direction=DOWN
        )

        BC00 = r"\(BC^2 = (3 - 3)^2 + (0 - 6)^2 + (9 - 3)^2\)"
        BC01 = r"\(BC^2 = 0^2 + 6^2 + 6^2\)"
        BC02 = r"\(BC^2 = 2\times 6^2\)"
        BC03 = r"\(BC^2 = AB^2 + AC^2\)"
        
        BC = [BC00, BC01, BC02, BC03]
        dBC = [Tex(d).scale(0.75) for d in BC]

        disp_calculations(self, 
            previous_mobj=None,
            calcs=dBC,
            next2obj=dAC[-1],
            direction=DOWN
        )

        self.play(
            dAC[-1].animate.next_to(dAB[-1], RIGHT)
        )
        self.wait()
        self.play(
            dBC[-1].animate.next_to(dAC[-1], RIGHT)
        )
        self.wait()

        q1 = Tex(r"1. ABC est un triangle : ")
        a = r"a. isocèle rectangle en A"
        b = r"b. isocèle rectangle en B"
        c = r"c. isocèle rectangle en C"
        d = r"d. équilatéral"
        m1 = MobjectMatrix(
            [[Tex(a), Tex(b)], [Tex(c), Tex(d)]],
            v_buff=2.5,
            h_buff=8,
            left_bracket="\{",
            right_bracket="\}"
        ).next_to(q1, DOWN)

        mobj1 = VGroup(q1, m1).scale(0.75)
        
        self.play(
            Write(mobj1.next_to(dAC[-1], DOWN).scale(0.75)),
        )
        self.wait()

        ent = m1.get_entries()
        sol_a = ent[0]
        box_a = SurroundingRectangle(sol_a, color=GREEN)

        self.play(
            Write(box_a)
        )
        self.wait()


# Question 2
class USAExo3Question2(Scene):
    def construct(self):
        msg1 = "Bac USA 27 mars 2023 Sujet 1 Exercice 3"
        title1 = Title(f"{msg1}")
        self.add(title1.scale(1))
        self.wait(2)

        intro = [
            r"L'espace est muni d'un repère orthonormé \((O; \vec{\imath}, \vec{\jmath}, \vec{k})\).",
            r"On considère les points \(A(-1;2;5)\), \(B(3; 6; 3)\), \(C(3; 0; 9)\) et \(D(8; -3; -8)\).",
            r"On admet que les points A, B, et C ne sont pas alignés."
        ]

        intro_tex = [Tex(i) for i in intro]
        self.play(
            Write(intro_tex[0].scale(0.75).next_to(title1, DOWN))
        )
        self.wait()
        for i in range(len(intro) - 1):
            self.play(
                Write(intro_tex[i+1].scale(0.75).next_to(intro_tex[i], DOWN))
            )
            self.wait()

        question2 = Title("Question 2")
        q2 = Tex(r"2. Une équation cartésienne du plan (BCD) est : ")
        a = r"a. \(2x + y + z - 15 = 0\)"
        b = r"b. \(9x - 5y + 3 = 0\)"
        c = r"c. \(4x + y + z - 21 = 0\)"
        d = r"d. \(11x + 5z - 73 = 0\)"
        m1 = MobjectMatrix(
            [[Tex(a), Tex(b)], [Tex(c), Tex(d)]],
            v_buff=2.5,
            h_buff=8,
            left_bracket="\{",
            right_bracket="\}"
        ).next_to(q2, DOWN)

        mobj1 = VGroup(q2, m1).scale(0.75)
        
        self.play(
            ReplacementTransform(title1, question2),
            Write(mobj1.next_to(intro_tex[-1], DOWN))
        )
        self.wait(4)

        noter = Title("Mettez pause pour noter la question")
        self.play(
            ReplacementTransform(question2, noter)
        )
        self.wait(4)

        attention_rep = Title("Cherchez avant de regarder le corrigé")
        self.play(
            ReplacementTransform(noter, attention_rep)
        )
        self.wait(4)

        ent = m1.get_entries()
        sol_c = ent[2]
        box_c = SurroundingRectangle(sol_c)
        solution2 = Title("Réponse c")
        self.play(
            ReplacementTransform(attention_rep, solution2),
            Write(box_c)
        )
        self.wait()

        
        explanation = Title("Explications")

        wrong_a = VGroup(ent[0])
        box_a = SurroundingRectangle(wrong_a, color=RED)
        
        self.play(
            ReplacementTransform(solution2, explanation),
            ReplacementTransform(box_c, box_a),
        )
        self.wait(2)

        
        aBCD00 = r"\(2x_D + y_D + z_D - 15 = 2\times 8 - 3 - 8 - 15\)"
        aBCD01 = r"\(2x_D + y_D + z_D - 15 = 16 - 11 - 15\)"
        aBCD02 = r"\(2x_D + y_D + z_D - 15 = - 10\neq 0\)"
        
        aBCD = [aBCD00, aBCD01, aBCD02]
        aBCDw = [Tex(d).scale(0.75) for d in aBCD]

        disp_calculations(self, 
            previous_mobj=None,
            calcs=aBCDw,
            next2obj=mobj1,
            direction=DOWN
        )

        wrong_b = VGroup(ent[1])
        box_b = SurroundingRectangle(wrong_b, color=RED)
        
        self.play(
            ReplacementTransform(box_a, box_b),
        )
        self.wait(2)

        
        bBCD00 = r"\(9x_C - 5y_C + 3 = 9\times 3 - 5\times 0 + 3\)"
        bBCD01 = r"\(9x_C - 5y_C + 3 = 27 - 0 + 3\)"
        bBCD02 = r"\(9x_C - 5y_C + 3 = 30 \neq 0\)"
        
        bBCD = [bBCD00, bBCD01, bBCD02]
        bBCDw = [Tex(d).scale(0.75) for d in bBCD]

        disp_calculations(self, 
            previous_mobj=aBCDw[-1],
            calcs=bBCDw,
            next2obj=mobj1,
            direction=DOWN
        )

        wrong_d = VGroup(ent[3])
        box_d = SurroundingRectangle(wrong_d, color=RED)
        
        self.play(
            ReplacementTransform(box_b, box_d),
        )
        self.wait(2)

        
        dBCD00 = r"\(11x_C + 5z_C - 73 = 11\times 3 + 5\times 9 - 73\)"
        dBCD01 = r"\(11x_C + 5z_C - 73 = 33 + 45 - 73\)"
        dBCD02 = r"\(11x_C + 5z_C - 73 = 5 \neq 0\)"
        
        dBCD = [dBCD00, dBCD01, dBCD02]
        dBCDw = [Tex(d).scale(0.75) for d in dBCD]

        disp_calculations(self, 
            previous_mobj=bBCDw[-1],
            calcs=dBCDw,
            next2obj=mobj1,
            direction=DOWN
        )

        right_c = VGroup(ent[2])
        box_c = SurroundingRectangle(right_c, color=GREEN)
        
        self.play(
            ReplacementTransform(box_d, box_c),
        )
        self.wait(2)

        
        B00 = r"\(4x_B + y_B + z_B - 21 = 4\times 3 + 6 + 3 - 21\)"
        B01 = r"\(4x_B + y_B + z_B - 21 = 12 + 6 + 3 - 21\)"
        B02 = r"\(4x_B + y_B + z_B - 21 = 0\)"
        
        B = [B00, B01, B02]
        Br = [Tex(d).scale(0.75) for d in B]

        disp_calculations(self, 
            previous_mobj=dBCDw[-1],
            calcs=Br,
            next2obj=mobj1,
            direction=DOWN
        )

        self.play(
            Br[-1].animate.shift(5*LEFT).scale(0.75)
        )
        self.wait()

        C00 = r"\(4x_C + y_C + z_C - 21 = 4\times 3 + 0 + 9 - 21\)"
        C01 = r"\(4x_C + y_C + z_C - 21 = 12 + 9 - 21\)"
        C02 = r"\(4x_C + y_C + z_C - 21 = 0\)"
        
        C = [C00, C01, C02]
        Cr = [Tex(d).scale(0.75) for d in C]

        disp_calculations(self, 
            previous_mobj=None,
            calcs=Cr,
            next2obj=mobj1,
            direction=DOWN
        )

        self.play(
            Cr[-1].animate.next_to(Br[-1], RIGHT).scale(0.75)
        )
        self.wait()

        D00 = r"\(4x_D + y_D + z_D - 21 = 4\times 8 + (-3) + (-8) - 21\)"
        D01 = r"\(4x_D + y_D + z_D - 21 = 32 - 11 - 21\)"
        D02 = r"\(4x_D + y_D + z_D - 21 = 0\)"
        
        D = [D00, D01, D02]
        Dr = [Tex(d).scale(0.75) for d in D]

        disp_calculations(self, 
            previous_mobj=None,
            calcs=Dr,
            next2obj=mobj1,
            direction=2.5 * DOWN
        )

        self.play(
            Dr[-1].animate.next_to(Cr[-1], RIGHT).scale(0.75)
        )
        self.wait()


# Question 3
class USAExo3Question3(Scene):
    def construct(self):
        msg1 = "Bac USA 27 mars 2023 Sujet 1 Exercice 3"
        title1 = Title(f"{msg1}")
        self.add(title1.scale(1))
        self.wait(2)

        intro = [
            r"L'espace est muni d'un repère orthonormé \((O; \vec{\imath}, \vec{\jmath}, \vec{k})\).",
            r"On considère les points \(A(-1;2;5)\), \(B(3; 6; 3)\), \(C(3; 0; 9)\) et \(D(8; -3; -8)\)."
        ]

        intro_tex = [Tex(i) for i in intro]
        self.play(
            Write(intro_tex[0].scale(0.75).next_to(title1, DOWN))
        )
        self.wait()
        for i in range(len(intro) - 1):
            self.play(
                Write(intro_tex[i+1].scale(0.75).next_to(intro_tex[i], DOWN))
            )
            self.wait()

        question3 = Title("Question 3").scale(0.75)
        q3_txt = [
            r"3. On admet que le plan (ABC) a pour équation cartésienne \(x - 2y - 2z + 15 = 0\).",
            r"On appelle H le projeté orthogonal du point D sur le plan (ABC).",
            r"On peut affirmer que : "
        ]
        q3 = [Tex(r).scale(0.75) for r in q3_txt]

        disp_tex_list(self, 
            previous_mobj=None,
            tex_list=q3,
            next2obj=intro_tex[-1],
            direction=DOWN
        )
        
        a = r"a. \(H(-2; 17; 12)\)"
        b = r"b. \(H(3; 7; 2)\)"
        c = r"c. \(H(3; 2; 7)\)"
        d = r"d. \(H(-15; 1; -1)\)"
        
        m1 = MobjectMatrix(
            [[Tex(a), Tex(b)], [Tex(c), Tex(d)]],
            v_buff=1.5,
            h_buff=8,
            left_bracket="\{",
            right_bracket="\}"
        ).scale(0.65)

        
        self.play(
            ReplacementTransform(title1, question3),
            Write(m1.next_to(q3[-1], DOWN))
        )
        self.wait(4)

        noter = Title("Mettez pause pour noter la question")
        self.play(
            ReplacementTransform(question3, noter)
        )
        self.wait(4)

        attention_rep = Title("Cherchez avant de regarder le corrigé")
        self.play(
            ReplacementTransform(noter, attention_rep)
        )
        self.wait(4)

        ent = m1.get_entries()
        sol_b = ent[1]
        box_b = SurroundingRectangle(sol_b)
        solution3 = Title("Réponse b")
        self.play(
            ReplacementTransform(attention_rep, solution3),
            Write(box_b)
        )
        self.wait()

        
        explanation = Title("Explications")

        wrong_a = VGroup(ent[0])
        box_a = SurroundingRectangle(wrong_a, color=RED)
        
        self.play(
            ReplacementTransform(solution3, explanation),
            ReplacementTransform(box_b, box_a),
        )
        self.wait(2)

        
        aWR00 = r"\(x_H - 2y_H - 2z_H + 15 = -2 - 2\times 17 - 2\times 12 + 15\)"
        aWR01 = r"\(x_H - 2y_H - 2z_H + 15 = -2 - 34 - 24 + 15\)"
        aWR02 = r"\(x_H - 2y_H - 2z_H + 15 = -45 \neq 0\)"
        aWR03 = r"Dans ce cas \(H\notin (ABC)\)"
        
        aWR = [aWR00, aWR01, aWR02, aWR03]
        aWRg = [Tex(d).scale(0.75) for d in aWR]

        disp_calculations(self, 
            previous_mobj=None,
            calcs=aWRg,
            next2obj=m1,
            direction=DOWN
        )

        wrong_c = VGroup(ent[2])
        box_c = SurroundingRectangle(wrong_c, color=RED)
        
        self.play(
            ReplacementTransform(box_a, box_c),
        )
        self.wait(2)

        
        cWR00 = r"\(x_H - 2y_H - 2z_H + 15 = 3 - 2\times 2 - 2\times 7 + 15\)"
        cWR01 = r"\(x_H - 2y_H - 2z_H + 15 = 3 - 4 - 14 + 15\)"
        cWR02 = r"\(x_H - 2y_H - 2z_H + 15 = 0\)"
        cWR03 = r"Dans ce cas \(H\in (ABC)\)"
        
        cWR = [cWR00, cWR01, cWR02, cWR03]
        cWRg = [Tex(d).scale(0.75) for d in cWR]

        disp_calculations(self, 
            previous_mobj=aWRg[-1],
            calcs=cWRg,
            next2obj=m1,
            direction=DOWN
            )
        
        self.play(
            cWRg[-1].animate.shift(5 * LEFT)
        )
        self.wait()
                          
        cDH00 = r"\(\overrightarrow{DH}(x_H - x_D; y_H - y_D; z_H - z_D)\)"
        cDH01 = r"\(\overrightarrow{DH}(3 - 8; 2 - (-3); 7 - (-8))\)"
        cDH02 = r"\(\overrightarrow{DH}(-5; 5; 15)\)"
        cDH03 = r"Ce vecteur n'est pas normal au plan (ABC)."
        cDH04 = r"Sinon il serait colinéaire à \(\vec{n}(1; -2; -2)\)"
        cDH05 = r"Il n'existe aucun réel \(k\) tel que \(\overrightarrow{DH} = k\vec{n}\)"
        cDH = [cDH00, cDH01, cDH02, cDH03, cDH04, cDH05]
        cDHg = [Tex(d).scale(0.75) for d in cDH]

        disp_calculations(self, 
            previous_mobj=None,
            calcs=cDHg,
            next2obj=m1,
            direction=2 * DOWN
            )

        
        wrong_d = VGroup(ent[3])
        box_d = SurroundingRectangle(wrong_d, color=RED)
        
        self.play(
            ReplacementTransform(box_c, box_d),
            FadeOut(cDHg[-1], cWRg[-1])
        )
        self.wait(2)

        
        dWR00 = r"\(x_H - 2y_H - 2z_H + 15 = -15 - 2\times 1 - 2\times (-1) + 15\)"
        dWR01 = r"\(x_H - 2y_H - 2z_H + 15 = -15 - 2 + 2 + 15\)"
        dWR02 = r"\(x_H - 2y_H - 2z_H + 15 = 0\)"
        dWR03 = r"Dans ce cas \(H\in (ABC)\)"
        
        dWR = [dWR00, dWR01, dWR02, dWR03]
        dWRg = [Tex(d).scale(0.75) for d in dWR]

        disp_calculations(self, 
            previous_mobj=None,
            calcs=dWRg,
            next2obj=m1,
            direction=DOWN
            )
        
        self.play(
            dWRg[-1].animate.shift(5 * LEFT)
        )
        self.wait()
                          
        dDH00 = r"\(\overrightarrow{DH}(x_H - x_D; y_H - y_D; z_H - z_D)\)"
        dDH01 = r"\(\overrightarrow{DH}(-15 - 8; 1 - (-3); (-1) - (-8))\)"
        dDH02 = r"\(\overrightarrow{DH}(-23; 4; 7)\)"
        dDH03 = r"Ce vecteur n'est pas normal au plan (ABC)."
        dDH04 = r"Sinon il serait colinéaire à \(\vec{n}(1; -2; -2)\)"
        dDH05 = r"Il n'existe aucun réel \(k\) tel que \(\overrightarrow{DH} = k\vec{n}\)"
        dDH = [dDH00, dDH01, dDH02, dDH03, dDH04, dDH05]
        dDHg = [Tex(d).scale(0.75) for d in dDH]

        disp_calculations(self, 
            previous_mobj=None,
            calcs=dDHg,
            next2obj=m1,
            direction=2 * DOWN
            )


        right_b = VGroup(ent[1])
        box_b = SurroundingRectangle(right_b, color=GREEN)
        
        self.play(
            ReplacementTransform(box_d, box_b),
            FadeOut(dDHg[-1], dWRg[-1])
        )
        self.wait(2)

        
        B00 = r"\(x_H - 2y_H - 2z_H + 15 = 3 - 2\times 7 - 2\times 2 + 15\)"
        B01 = r"\(x_H - 2y_H - 2z_H + 15 = 3 - 14 - 4 + 15\)"
        B02 = r"\(x_H - 2y_H - 2z_H + 15 = 0\)"
        B03 = r"Dans ce cas \(H\in (ABC)\)"
        B = [B00, B01, B02, B03]
        Br = [Tex(d).scale(0.75) for d in B]

        disp_calculations(self, 
            previous_mobj=None,
            calcs=Br,
            next2obj=m1,
            direction=DOWN
        )

        self.play(
            Br[-1].animate.shift(2*LEFT).scale(0.75)
        )
        self.wait()

        bDH00 = r"\(\overrightarrow{DH}(x_H - x_D; y_H - y_D; z_H - z_D)\)"
        bDH01 = r"\(\overrightarrow{DH}(3 - 8; 7 - (-3); 2 - (-8))\)"
        bDH02 = r"\(\overrightarrow{DH}(-5; 10; 10)\)"
        bDH03 = r"Ce vecteur est normal au plan (ABC)."
        bDH04 = r"Il est colinéaire à \(\vec{n}(1; -2; -2)\)"
        bDH05 = r"\(\overrightarrow{DH} = -5\vec{n}\)"
        bDH = [bDH00, bDH01, bDH02, bDH03, bDH04, bDH05]
        bDHg = [Tex(d).scale(0.75) for d in bDH]

        disp_calculations(self, 
            previous_mobj=None,
            calcs=bDHg,
            next2obj=m1,
            direction=2 * DOWN
            )

        self.play(
            bDHg[-1].scale(0.75).animate.next_to(Br[-1], RIGHT)
        )
        self.wait()

# Question 4
class USAExo3Question4(Scene):
    def construct(self):
        msg1 = "Bac USA 27 mars 2023 Sujet 1 Exercice 3"
        title1 = Title(f"{msg1}")
        self.add(title1.scale(1))
        self.wait(2)

        intro = [
            r"L'espace est muni d'un repère orthonormé \((O; \vec{\imath}, \vec{\jmath}, \vec{k})\).",
            r"On considère les points \(A(-1;2;5)\), \(B(3; 6; 3)\), \(C(3; 0; 9)\) et \(D(8; -3; -8)\).",
            r"On admet que les points A, B et C ne sont pas alignés."
        ]

        intro_tex = [Tex(i).scale(0.65) for i in intro]
        self.play(
            Write(intro_tex[0].next_to(title1, DOWN))
        )
        self.wait()
        for i in range(len(intro) - 1):
            self.play(
                Write(intro_tex[i+1].next_to(intro_tex[i], DOWN))
            )
            self.wait()

        question4 = Title("Question 4").scale(0.65)
        q4_txt = [
            r"4. Soit la droite \(\Delta\) de représentation paramétrique \(\left\{\begin{aligned}x &= 5 + t\\y &= 3 - t\\ z &= -1 + 3t\end{aligned}\right.\), avec \(t\) réel." ,
            r"Les droites (BC) et \(\Delta\) sont : ",
        ]
        q4 = [Tex(r).scale(0.65) for r in q4_txt]

        disp_tex_list(self, 
            previous_mobj=None,
            tex_list=q4,
            next2obj=intro_tex[-1],
            direction=DOWN
        )
        
        a = r"a. confondues"
        b = r"b. strictement parallèles"
        c = r"c. sécantes"
        d = r"d. non coplanaires"
        
        m1 = MobjectMatrix(
            [
                [Tex(a), Tex(b)],
                [Tex(c), Tex(d)],
            ],
            v_buff=1.5,
            h_buff=8,
            left_bracket="\{",
            right_bracket="\}"
        ).scale(0.65)

        
        self.play(
            ReplacementTransform(title1, question4),
            Write(m1.next_to(q4[-1], DOWN))
        )
        self.wait(4)

        noter = Title("Mettez pause pour noter la question")
        self.play(
            ReplacementTransform(question4, noter)
        )
        self.wait(4)

        attention_rep = Title("Cherchez avant de regarder le corrigé")
        self.play(
            ReplacementTransform(noter, attention_rep)
        )
        self.wait(4)

        ent = m1.get_entries()
        sol_c = ent[2]
        box_c = SurroundingRectangle(sol_c)
        solution4 = Title("Réponse c")
        self.play(
            ReplacementTransform(attention_rep, solution4),
            Write(box_c)
        )
        self.wait()

        
        explanation = Title("Explications")
        cRight00 = r"\(\Delta\) est dirigée par \(\vec{u}(1;-1;3)\)."
        cRight01 = r"\(\overrightarrow{BC}(x_C - x_B; y_C - y_B; z_C - z_B)\)"
        cRight02 = r"\(\overrightarrow{BC}(3 - 3; 0 - 2; 9 - 3)\)"
        cRight03 = r"\(\overrightarrow{BC}(0; -2; 6)\)"
        cRight04 = r"Les vecteurs directeurs ne sont pas colinéaires."
        cRight05 = r"Donc les droites sont sécantes."
        cRight = [cRight00, cRight01, cRight02, cRight03, cRight04, cRight05]
        Cr = [Tex(r).scale(0.65) for r in cRight]
        disp_calculations(self, 
            previous_mobj=None,
            calcs=Cr,
            next2obj=m1,
            direction=DOWN
            )



# Question 5
class USAExo3Question5(Scene):
    def construct(self):
        msg1 = "Bac USA 27 mars 2023 Sujet 1 Exercice 3"
        title1 = Title(f"{msg1}")
        self.add(title1.scale(1))
        self.wait(2)

        intro = [
            r"L'espace est muni d'un repère orthonormé \((O; \vec{\imath}, \vec{\jmath}, \vec{k})\).",
            r"On considère les points \(A(-1;2;5)\), \(B(3; 6; 3)\), \(C(3; 0; 9)\) et \(D(8; -3; -8)\).",
            r"On admet que les points A, B et C ne sont pas alignés."
        ]
        intro_tex = [Tex(i).scale(0.55) for i in intro]

        self.play(
            Write(intro_tex[0].next_to(title1, DOWN))
        )
        self.wait()
        
        for i in range(len(intro) - 1):
            self.play(
                Write(intro_tex[i+1].next_to(intro_tex[i], DOWN))
            )
            self.wait()

        question5 = Title("Question 5").scale(0.55)
        q5_00 = r"5. On considère le plan \(\mathcal{P}\) "
        q5_00 += r"d'équation cartésienne \(2x - y + 2z - 6 = 0\)."
        q5_01 = r"On admet que le plan (ABC) a pour équation "
        q5_01 += r"cartésienne \(x - 2y - 2z + 15 = 0\)."
        q5_02 = r"On peut affirmer que : "
        q5_txt = [q5_00, q5_01, q5_02]
        q5 = [Tex(r).scale(0.55) for r in q5_txt]

        disp_tex_list(self, 
            previous_mobj=None,
            tex_list=q5,
            next2obj=intro_tex[-1],
            direction=DOWN
        )
        
        a = r"a. les plans \(\mathcal{P}\) et (ABC) sont strictement parallèles"
        
        b = r"b. les plans \(\mathcal{P}\) et (ABC) sont sécants et leur "
        b += r"intersection est la droite (AB)"
        
        c = r"c. les plans \(\mathcal{P}\) et (ABC) sont sécants et leur "
        c += r"intersection est la droite (AC)"
        
        d = r"d. les plans \(\mathcal{P}\) et (ABC) sont sécants et leur "
        d += r"intersection est la droite (BC)"
        
        m1 = MobjectMatrix(
            [
                [Tex(a)],
                [Tex(b)],
                [Tex(c)],
                [Tex(d)],
            ],
            v_buff=.75,
            h_buff=8,
            left_bracket="\{",
            right_bracket="\}"
        ).scale(0.55)

        
        self.play(
            ReplacementTransform(title1, question5),
            Write(m1.next_to(q5[-1], DOWN))
        )
        self.wait(4)

        noter = Title("Mettez pause pour noter la question")
        self.play(
            ReplacementTransform(question5, noter)
        )
        self.wait(4)

        attention_rep = Title("Cherchez avant de regarder le corrigé")
        self.play(
            ReplacementTransform(noter, attention_rep)
        )
        self.wait(4)

        ent = m1.get_entries()
        sol_b = ent[1]
        box_b = SurroundingRectangle(sol_b)
        solution5 = Title("Réponse b")
        self.play(
            ReplacementTransform(attention_rep, solution5),
            Write(box_b)
        )
        self.wait()

        
        explanation = Title("Explications")
        self.play(ReplacementTransform(solution5, explanation))
        self.wait()
        
        bRight00 = r"Pour déterminer l'intersection entre plans"
        bRight01 = r"il faut résoudre le système d'équations "
        bRight02 = r"\(\left\{\begin{aligned}2x - y + 2z - 6 &= 0\\x - 2y - 2z + 15 &= 0\end{aligned}\right.\)"
        bRight03 = r"La seconde équation permet d'obtenir \(x = 2y + 2z - 15\)"
        bRight04 = r"En substituant cette expression dans la première équation "
        bRight05 = r"\(2(2y + 2z - 15) - y + 2z - 6 = 0\)"
        bRight06 = r"On obtient : \(3y + 6z - 36 = 0\)"
        bRight07 = r"D'où : \(y = -2z + 12\)"
        bRight08 = r"Finalement on obtient le système : \(\left\{\begin{aligned}x &= -2t + 9\\y &= -2t + 12\\ z &= t\end{aligned}\right.\)"
        bRight = [
            bRight00,
            bRight01,
            bRight02,
            bRight03,
            bRight04,
            bRight05,
            bRight06,
            bRight07,
            bRight08
        ]
        Br = [Tex(r).scale(0.6) for r in bRight]
        disp_calculations(self, 
            previous_mobj=None,
            calcs=Br,
            next2obj=m1,
            direction=DOWN
            )

        self.play(
            Br[-1].animate.shift(3.5 * LEFT)
        )
        self.wait()

        AB00 = r"\(\overrightarrow{AB}(x_B - x_A; y_B - y_A; z_B - z_A)\)"
        AB01 = r"\(\overrightarrow{AB}(3 - (-1); 6 - 2; 3 - 5)\)"
        AB02 = r"\(\overrightarrow{AB}(4; 4; -2) = -2(-2; -2; 1)\)"
        AB03 = r"Avec \(t = 3\) on obtient B et avec \(t = 5\) on obtient A"
        AB = [AB00, AB01, AB02, AB03]
        ABr = [Tex(r).scale(0.6) for r in AB]
        disp_calculations(self, 
            previous_mobj=None,
            calcs=ABr,
            next2obj=Br[-1],
            direction=RIGHT
            )

        self.play(
            ABr[-1].animate.next_to(Br[-1], RIGHT)
        )
        self.wait()

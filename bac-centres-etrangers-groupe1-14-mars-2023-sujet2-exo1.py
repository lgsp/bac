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
# Centres étrangers Groupe 1 Sujet 2
##################################################

# Exo 1
class ForeignCenterExo1Question1(Scene):
    def construct(self):
        msg1 = "Bac 2023 centres étrangers groupe 1 sujet 2"
        title1 = Title(f"{msg1}")
        self.add(title1.scale(1))
        self.wait(2)
        
        question1 = Title("Question 1 : primitive d'une fonction")
        self.play(
            ReplacementTransform(title1, question1)
        )
        self.wait()
        

        q1_txt = r"Soit \(f\) la fonction définie sur \(\mathbb{R}\) par "
        q1_txt += r"\(f(x) = xe^x\)."
        q1 = Tex(q1_txt).scale(0.75)

        q1_txt2 = r"Une primitive \(F\) sur \(\mathbb{R}\) de la fonction "
        q1_txt2 += r"\(f\) est définie par :"
        q1_q = Tex(q1_txt2).next_to(q1, DOWN).scale(0.75)

        a = Tex(r"A.\(F(x) = \dfrac{x^2}{2}e^x\)")
        b = Tex(r"B.\(F(x) = (x - 1)e^x\)")
        c = Tex(r"C.\(F(x) = (x + 1)e^x\)")
        d = Tex(r"D.\(F(x) = \dfrac{2}{x}e^{x^2}\)")
        
        m1 = MobjectMatrix(
            [[a, b], [c, d]],
            v_buff=2.5,
            h_buff=5,
            left_bracket="\{",
            right_bracket="\}"
        ).next_to(q1_q, DOWN).scale(0.75)
        
        mobj1 = VGroup(q1, q1_q, m1)


        self.play(
            Write(mobj1.next_to(title1, 1.75 * DOWN))
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
        sol_B = ent[1]
        box_B = SurroundingRectangle(sol_B)
        solution1 = Title("Réponse B")
        self.play(
            ReplacementTransform(attention_rep, solution1),
            Write(box_B)
        )
        self.wait()
        
        r1 = r"Rappel : \( (uv)' = u'v + uv'\)"
        r12 = r"Pour \(F(x) = (x-1)e^x\) posons \(u = x - 1\) et \(v = e^x\)"
        r13 = r"Ainsi \(u' = 1\) et \(v' = e^x\)"
        r14 = r"D'où \(F'(x) = e^x + (x - 1)e^x = e^x + xe^x - e^x\)"
        r15 = r"Finalement \(F'(x) = xe^x = f(x)\) CQFD"
        
        rep = [r1, r12, r13, r14, r15]
        p = [Tex(r) for r in rep]

        explanation = Title("Explications")
        self.play(
            Unwrite(box_B),
            ReplacementTransform(solution1, explanation),
            ReplacementTransform(mobj1, p[0].next_to(title1, 2 * DOWN))
        )
        self.wait()

        for i in range(1, len(p)):
            self.play(Write(p[i].next_to(p[i-1], DOWN)))
            self.wait(2)
        

        

class ForeignCenterExo1Question2(Scene):
    def construct(self):
        msg1 = "Bac 2023 centres étrangers groupe 1 sujet 2"
        title1 = Title(f"{msg1}")
        self.add(title1.scale(1))
        self.wait(2)
        
        question2 = Title("Question 2 : Dérivées d'une fonction")
        self.play(
            ReplacementTransform(title1, question2)
        )
        self.wait()
        

        q1_txt = r"La courbe \(\mathcal{C}\) ci-dessous représente une "
        q1_txt += r"fonction \(f\) définie et deux fois dérivable "
        q1_txt += r"sur \(]0;+\infty[\). On sait que :"
        q1 = Tex(q1_txt).scale(0.75)

        q12 = r"\(\bullet\) le maximum de la fonction \(f\) est atteint "
        q12 += r"au point d'abscisse 3 ;"
        q1_q = Tex(q12).next_to(q1, DOWN).scale(0.7)
        q12bis = r"\(\bullet\) le point P d'abscisse 5 est l'unique point "
        q12bis += r"d'inflexion de la courbe \(\mathcal{C}\)."
        q1_qbis = Tex(q12bis).next_to(q1_q, DOWN).scale(0.7)

        mobj1 = VGroup(q1, q1_q, q1_qbis)
        self.play(Write(mobj1.next_to(title1, 0.25 * DOWN)))
        self.wait(2)
        
        ax = Axes(
            x_range=[0, 10, 1],
            y_range=[-2, 6, 1],
            x_axis_config={"numbers_to_include": np.arange(0, 10, 1)},
            y_axis_config={"numbers_to_include": np.arange(-2, 6, 1)},
        ).add_coordinates().scale(0.8)


        def func(x):
            return (x - 1) * e ** (2.31 - 0.5 * x)
        graph = ax.plot(
            func,
            x_range=[0.7, 10, 1],
            color=MAROON
        )

        
        tan_x_3 = ax.plot(lambda x: 4.5, x_range=[1, 5, 1], color=YELLOW)
        tan_x_5 = ax.plot(
            lambda x: (-3.25/4)*x + 29.25/4,
            x_range=[2, 9, 1], color=YELLOW
        )
        
        A = Dot(ax.coords_to_point(3, 4.5), color=GREEN)
        A_lines = ax.get_lines_to_point(ax.c2p(3, 4.5), color=GREEN)
        P = Dot(ax.coords_to_point(5, 3.25), color=GREEN)
        P_lines = ax.get_lines_to_point(ax.c2p(5, 3.25), color=GREEN)
        P_label = Text("P").next_to(P, 0.5*UR).scale(0.7).set_color(GREEN)

        mobj2 = VGroup(
            ax, graph, A, A_lines, tan_x_3, P, P_lines, P_label, tan_x_5
        )
        self.play(Write(mobj2.next_to(mobj1, 0.25 * DOWN)))
        self.wait(5)

        
        q1a = Tex(r"On a :").scale(0.75)
        repA11 = r"A. Pour tout \(x\in]0;5[\), "
        a11 = Tex(repA11)
        repA21 = r"\(f(x)\) et \(f'(x)\) sont de même signe"
        a21 = Tex(repA21)
        repB12 = r"B. Pour tout \(x\in]5;+\infty[\), "
        b12 = Tex(repB12)
        repB22 = r"\(f(x)\) et \(f'(x)\) sont de même signe"
        b22 = Tex(repB22)
        repC31 = r"C. Pour tout \(x\in]0;5[\), "
        c31 = Tex(repC31)
        repC41 = r"\(f'(x)\) et \(f''(x)\) sont de même signe"
        c41 = Tex(repC41)
        repD32 = r"D. Pour tout \(x\in]5;+\infty[\), "
        d32 = Tex(repD32)
        repD42 = r"\(f(x)\) et \(f''(x)\) sont de même signe"
        d42 = Tex(repD42)
        
        m1 = MobjectMatrix(
            [[a11, b12], [a21, b22], [c31, d32], [c41, d42]],
            v_buff=0.85,
            h_buff=10,
            left_bracket="\{",
            right_bracket="\}"
        ).next_to(q1a, 0.25*DOWN).scale(0.75)
        
        mobj3 = VGroup(q1a, m1)


        self.play(
            ReplacementTransform(mobj1, mobj3.next_to(mobj1, 3 * DOWN)),
            # mobj2.animate.next_to(title1, 0.015*DOWN).scale(0.75)
            mobj2.animate.shift(3 * UP).scale(0.7)
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

        
        solution1 = Title("Réponse D")

        # Version 1
        ent = m1.get_entries()
        sol_D1 = ent[5]
        sol_D2 = ent[7]
        sols_D = VGroup(sol_D1, sol_D2)

        # Version 2
        col1 = m1.get_columns()[1]
        sols_D2 = col1[2:]
        box_D = SurroundingRectangle(sols_D2)
        
        self.play(
            ReplacementTransform(attention_rep, solution1),
            Write(box_D)
        )
        self.wait(4)

        explanation = Title("Explications")
        
        wrong_A = VGroup(ent[0], ent[2])
        box_A = SurroundingRectangle(wrong_A, color=RED)
        
        self.play(
            ReplacementTransform(solution1, explanation),
            ReplacementTransform(box_D, box_A),
            mobj2.animate.shift(3.5 * LEFT),
        )
        self.wait(2)
        awrong_dict = {
            r"Pour tout \(x\in ]0;1], f(x)\leqslant 0\).": RED,
            r"Alors que la courbe est croissante sur \(]0;1]\).": GREEN,
            r"Donc \(f'(x) \geqslant 0\) sur \(]0;1]\).": GREEN,
            r"Pour tout \(x\in ]0;1], f(x)f'(x)\leqslant 0\).": RED
        }
        a_proof = [
            Tex(
                text,
                color=color
            ).scale(0.75) for text, color in awrong_dict.items()
        ]
        self.play(
            Write(
                a_proof[0].next_to(
                    explanation,
                    0.25 * DOWN
                )
            )
        )
        self.wait(2)
        for i in range(len(a_proof) - 1):
            self.play(
                Write(a_proof[i + 1].next_to(a_proof[i], 0.75 * DOWN))
            )
            self.wait(2)
        proofA = VGroup(*a_proof)
        self.play(proofA.animate.shift(2.5 * RIGHT))
        self.wait(4)

        wrong_B = VGroup(ent[1], ent[3])
        box_B = SurroundingRectangle(wrong_B, color=RED)
        
        self.play(
            ReplacementTransform(box_A, box_B),
            FadeOut(proofA)
        )
        self.wait()
        bwrong_dict = {
            r"Pour tout \(x\in [5;+\infty[, f(x)\geqslant 0\).": GREEN,
            r"Alors que la courbe est décroissante sur \([5;+\infty[\).": RED,
            r"Donc \(f'(x) \leqslant 0\) sur \([5;+\infty[\).": RED,
            r"Pour tout \(x\in [5;+\infty[, f(x)f'(x)\leqslant 0\).": RED
        }
        b_proof = [
            Tex(
                text,
                color=color
            ).scale(0.75) for text, color in bwrong_dict.items()
        ]
        self.play(
            Write(
                b_proof[0].next_to(
                    explanation,
                    0.25 * DOWN
                )
            )
        )
        self.wait(2)
        for i in range(len(b_proof) - 1):
            self.play(
                Write(b_proof[i + 1].next_to(b_proof[i], 0.75 * DOWN))
            )
            self.wait(2)
        proofB = VGroup(*b_proof)
        self.play(proofB.animate.shift(2.5 * RIGHT))
        self.wait(4)


        wrong_C = VGroup(ent[4], ent[6])
        box_C = SurroundingRectangle(wrong_C, color=RED)
        
        self.play(
            ReplacementTransform(box_B, box_C),
            FadeOut(proofB)
        )
        self.wait(2)
        cwrong_dict = {
            r"Pour tout \(x\in ]0;3], f'(x)\geqslant 0\).": GREEN,
            r"Alors que la courbe est concave sur \(]0;3]\).": RED,
            r"Donc \(f''(x) \leqslant 0\) sur \(]0;3]\).": RED,
            r"Pour tout \(x\in ]0;3], f'(x)f''(x)\leqslant 0\).": RED
        }
        c_proof = [
            Tex(
                text,
                color=color
            ).scale(0.75) for text, color in cwrong_dict.items()
        ]
        self.play(
            Write(
                c_proof[0].next_to(
                    explanation,
                    0.25 * DOWN
                )
            )
        )
        self.wait(2)
        for i in range(len(c_proof) - 1):
            self.play(
                Write(c_proof[i + 1].next_to(c_proof[i], 0.75 * DOWN))
            )
            self.wait(2)
        proofC = VGroup(*c_proof)
        self.play(proofC.animate.shift(2.5 * RIGHT))
        self.wait(4)

        right_D = VGroup(ent[5], ent[7])
        box_D = SurroundingRectangle(right_D, color=GREEN)
        
        self.play(
            ReplacementTransform(box_C, box_D),
            FadeOut(proofC)
        )
        self.wait(2)
        dwrong_dict = {
            r"Pour tout \(x\in ]5;+\infty[, f(x)\geqslant 0\).": GREEN,
            r"La courbe est convexe sur \(]5;+\infty[\).": GREEN,
            r"Donc \(f''(x) \geqslant 0\) sur \(]5;+\infty[\).": GREEN,
            r"Pour tout \(x\in ]5;+\infty[, f(x)f''(x)\geqslant 0\).": GREEN
        }
        d_proof = [
            Tex(
                text,
                color=color
            ).scale(0.75) for text, color in dwrong_dict.items()
        ]
        self.play(
            Write(
                d_proof[0].next_to(
                    explanation,
                    0.25 * DOWN
                )
            )
        )
        self.wait(2)
        for i in range(len(d_proof) - 1):
            self.play(
                Write(d_proof[i + 1].next_to(d_proof[i], 0.75 * DOWN))
            )
            self.wait(2)
        proofD = VGroup(*d_proof)
        self.play(proofD.animate.shift(2.5 * RIGHT))
        self.wait(4)

class ForeignCenterExo1Question3(Scene):
    def construct(self):
        msg1 = "Bac 2023 centres étrangers groupe 1 sujet 2"
        title1 = Title(f"{msg1}")
        self.add(title1.scale(1))
        self.wait(2)

        t = "Question 3 : Identification de paramètres "
        question3 = Title(t)
        self.play(
            ReplacementTransform(title1, question3)
        )
        self.wait()
        

        q01_txt = r"On considère une fonction \(g\) "
        q01_txt += r"définie sur \([0;+\infty[\) par "
        q01_txt += r"\[g(t) = \dfrac{a}{b+e^{-t}}\] "
        q01_txt += r"où \(a\) et \(b\) sont deux réels. "
        q01_txt += r"On sait que "
        q01 = Tex(q01_txt)
    
        q11_txt = r"\(g(0) = 2\) et "
        q11_txt += r"\(\lim_{t\to +\infty}g(t) = 3\)"
        q11 = Tex(q11_txt).next_to(q01, DOWN)

        mobj1 = VGroup(q01, q11).scale(0.75)
        
        self.play(
            Write(mobj1.next_to(title1, DOWN))
        )
        self.wait()

        intro_q = Tex(r"Les valeurs de \(a\) et \(b\) sont : ").scale(0.75)
        repA = r"A. \(a = 2\) et \(b = 3\)"
        A = Tex(repA)
        repB = r"B. \(a = 4\) et \(b = \dfrac{4}{3}\)"
        B = Tex(repB)
        repC = r"C. \(a = 4\) et \(b = 1\)"
        C = Tex(repC)
        repD = r"D. \(a = 6\) et \(b = 2\)"
        D = Tex(repD)
        m1 = MobjectMatrix(
            [[A, B], [C, D]],
            v_buff=1,
            h_buff=8,
            left_bracket="\{",
            right_bracket="\}"
        ).next_to(intro_q, DOWN).scale(0.75)

        mobj2 = VGroup(intro_q, m1)
        self.play(
            Write(mobj2.next_to(mobj1, DOWN))
        )
        self.wait()
        
        

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
        
        solution1 = Title("Réponse D")
        ent = m1.get_entries()
        sol_D = ent[3]
        box_D = SurroundingRectangle(sol_D)
        self.play(
            ReplacementTransform(attention_rep, solution1),
            Write(box_D)
        )
        self.wait(4)
        
        explanation = Title("Explications")

        g00 = r"g(0) = 2"
        g01 = r"\dfrac{a}{b + e^{-0}} = 2"
        g02 = r"\dfrac{a}{b + 1} = 2"
        g03 = r"a = 2(b + 1)"
        g04 = r"a = 2b + 2"
        g0 = [MathTex(g).scale(0.75) for g in [g00, g01, g02, g03, g04]]

        
        self.play(
            ReplacementTransform(solution1, explanation),
            ReplacementTransform(mobj1, g0[0].next_to(solution1, DOWN))
        )
        self.wait()

        for i in range(len(g0) - 1):
            self.play(
                ReplacementTransform(g0[i], g0[i+1].next_to(solution1, DOWN))
            )
            self.wait(2)

        box1 = SurroundingRectangle(g0[-1])
        g0_final = Group(g0[-1], box1)
        self.play(
            Write(box1),
            g0_final.animate.shift(4 * LEFT)
        )
        
        
        g_lim00 = r"\lim_{t\to +\infty}g(t) = 3"
        g_lim01 = r"\lim_{t\to +\infty}\dfrac{a}{b + e^{-t}} = 3"
        g_lim02 = r"\dfrac{a}{b} = 3"
        g_lim03 = r"a = 3b"
        g_lims = [g_lim00, g_lim01, g_lim02, g_lim03]
        g_lim0 = [MathTex(g).scale(0.75) for g in g_lims]
        self.play(
            Write(g_lim0[0].next_to(explanation, DOWN))
        )
        self.wait()

        for i in range(len(g_lim0) - 1):
            self.play(
                ReplacementTransform(
                    g_lim0[i],
                    g_lim0[i+1].next_to(explanation, DOWN)
                )
            )
            self.wait(2)

        box2 = SurroundingRectangle(g_lim0[-1])
        g_lim0_final = Group(g_lim0[-1], box2)
        self.play(
            Write(box2),
            g_lim0_final.animate.shift(4 * RIGHT)
        )
        self.wait()

        merge00 = r"2b + 2 = 3b"
        merge01 = r"2 = b"
        merge02 = r"a = 6"
        merge03 = r"(a, b) = (6, 2)"
        
        merges = [merge00, merge01, merge02, merge03]
        merge0 = [MathTex(g).scale(0.75) for g in merges]
        self.play(
            ReplacementTransform(
                g0_final,
                merge0[0].next_to(explanation, DOWN)
            ),
            FadeOut(g_lim0_final)
        )
        self.wait()

        for i in range(len(merge0) - 1):
            self.play(
                ReplacementTransform(
                    merge0[i],
                    merge0[i+1].next_to(explanation, DOWN)
                )
            )
            self.wait(2)

        box3 = SurroundingRectangle(merge0[-1])
        merge0_final = Group(merge0[-1], box3)
        self.play(
            Write(box3)
        )
        self.wait()


class ForeignCenterExo1Question4(Scene):
    def construct(self):
        msg1 = "Bac 2023 centres étrangers groupe 1 sujet 2"
        title1 = Title(f"{msg1}")
        self.add(title1.scale(0.75))
        self.wait(2)
        
        question4 = Title("Question 4 : Probabilités").scale(0.75)
        self.play(
            ReplacementTransform(title1, question4)
        )
        self.wait()
        

        q41_txt = r"Alice dispose de deux urnes A et B contenant chacune "
        q41_txt += r"quatre boules indiscernables au toucher."
        q41 = Tex(q41_txt)
        
        q42_txt = r"L'urne A contient deux boules vertes et deux boules "
        q42_txt += r"rouges."
        q42 = Tex(q42_txt).next_to(q41, DOWN)

        q43_txt = r"L'urne B contient trois boules vertes et une boule "
        q43_txt += r"rouge."
        q43 = Tex(q43_txt).next_to(q42, DOWN)

        q44_txt = r"Alice choisit au hasard une urne puis une boule dans "
        q44_txt += r"cette urne. Elle obtient une boule verte."
        q44 = Tex(q44_txt).next_to(q43, DOWN)

        q45_txt = r"La probabilité qu'elle ait choisit l'urne B "
        q45_txt += r"est : "
        q45 = Tex(q45_txt).next_to(q44, DOWN)

        q4_list = [q41, q42, q43, q44, q45]
        q4 = VGroup(*q4_list).next_to(title1, DOWN)

        self.play(Write(q4.scale(0.75)))
        self.wait(2)

        self.play(q4.animate.shift(0.7 * UP))
        self.wait(2)
        
        A = MathTex(r"A. \dfrac{3}{8}")
        B = MathTex(r"B. \dfrac{1}{2}")
        C = MathTex(r"C. \dfrac{3}{5}")
        D = MathTex(r"D. \dfrac{5}{8}")

        m1 = MobjectMatrix(
            [[A, B], [C, D]],
            v_buff=2,
            h_buff=4,
            left_bracket="\{",
            right_bracket="\}"
        ).next_to(q4, DOWN).scale(0.75)

        self.play(
            Write(m1),
            m1.animate.shift(0.5*UP)
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
        sol_C = ent[2]
        box_C = SurroundingRectangle(sol_C)
        solution1 = Title("Réponse C")

        self.play(
            ReplacementTransform(attention_rep, solution1),
            Write(box_C)
        )
        self.wait(2)

        explanation = Title("Explications")

        plane = ComplexPlane()
        O = Dot(plane.n2p(0 + 0j), color=YELLOW)
        A = Dot(plane.n2p(2 + 2j), color=YELLOW)
        labelA = MathTex("A").next_to(A, RIGHT)
        B = Dot(plane.n2p(2 - 2j), color=YELLOW)
        labelB = MathTex("B").next_to(B, RIGHT)
        OA = Line(O, A)
        OB = Line(O, B)
        
        V_1 = Dot(plane.n2p(4 + 3j), color=GREEN)
        labelV_1 = MathTex("V", color=GREEN).next_to(V_1, RIGHT)
        R_1 = Dot(plane.n2p(4 + 1j), color=RED)
        labelR_1 = MathTex("R", color=RED).next_to(R_1, RIGHT)
        AV = Line(A, V_1)
        AR = Line(A, R_1)
        
        R_2 = Dot(plane.n2p(4 - 3j), color=RED)
        labelR_2 = MathTex("R", color=RED).next_to(R_2, RIGHT)
        V_2 = Dot(plane.n2p(4 - 1j), color=GREEN)
        labelV_2 = MathTex("V", color=GREEN).next_to(V_2, RIGHT)
        BV = Line(B, V_2)
        BR = Line(B, R_2)
        
        proba_tree = VGroup(
            O,
            A, labelA,
            B, labelB,
            OA, OB,
            V_1, labelV_1,
            R_1, labelR_1,
            AV, AR,
            R_2, labelR_2,
            V_2, labelV_2,
            BV, BR
        )
        
        self.play(
            ReplacementTransform(solution1, explanation),
            ReplacementTransform(m1, proba_tree.scale(0.5)),
            q4.animate.scale(0.75).shift(0.25*UP),
            FadeOut(box_C),
            proba_tree.animate.shift(2 * LEFT + 1.75 * DOWN)
        )
        self.wait(2)

        labelProbA = MathTex(
            "\dfrac{1}{2}",
            color=YELLOW
        ).next_to(A, 1.5 * LEFT).scale(0.5)
        labelProbB = MathTex(
            "\dfrac{1}{2}",
            color=YELLOW
        ).next_to(B, 1.5 * LEFT).scale(0.5)
        probs_label1 = [labelProbA, labelProbB]
        self.play(
            *[Write(pl) for pl in probs_label1]
        )
        self.wait()

        labelProbA_V = MathTex(
            "\dfrac{2}{4}",
            color=GREEN
        ).next_to(V_1, 1.5 * LEFT).scale(0.5)
        labelProbA_R = MathTex(
            "\dfrac{2}{4}",
            color=RED
        ).next_to(R_1, 1.5 * LEFT).scale(0.5)
        labelProbB_V = MathTex(
            "\dfrac{3}{4}",
            color=GREEN
        ).next_to(V_2, 1.5 * LEFT).scale(0.5)
        labelProbB_R = MathTex(
            "\dfrac{1}{4}",
            color=RED
        ).next_to(R_2, 1.5 * LEFT).scale(0.5)
        probs_label2 = [
            labelProbA_V, labelProbA_R,
            labelProbB_V, labelProbB_R
        ]
        self.play(
            *[Write(pl) for pl in probs_label2]
        )
        self.wait()

        labelProbAV = MathTex(
            "\Rightarrow P(A\cap V) = \dfrac{2}{8}",
            color=GREEN
        ).next_to(V_1, RIGHT).scale(0.5)
        labelProbBV = MathTex(
            "\Rightarrow P(B\cap V) = \dfrac{3}{8}",
            color=GREEN
        ).next_to(V_2, RIGHT).scale(0.5)
        probs_label3 = [labelProbAV, labelProbBV]
        self.play(
            *[Write(pl) for pl in probs_label3]
        )
        self.wait()

        V_tot = Dot(plane.n2p(6 + 0j), color=GREEN)
        labelprobV_tot = MathTex(
            "P(V) = \dfrac{5}{8}",
            color=GREEN
        ).next_to(labelProbAV, DOWN).scale(0.5)
        self.play(Write(labelprobV_tot))
        self.wait()
        
        probs_label1_group = VGroup(*probs_label1)
        probs_label2_group = VGroup(*probs_label2)
        probs_label3_group = VGroup(*probs_label3)

        full_proba_tree = VGroup(
            proba_tree,
            probs_label1_group,
            probs_label2_group,
            probs_label3_group,
            labelprobV_tot
        )

        probaBcondV00 = r"P_V(B) = \dfrac{P(B\cap V)}{P(V)}"
        probaBcondV01 = r"P_V(B) = \dfrac{\dfrac{3}{8}}{\dfrac{5}{8}}"
        probaBcondV02 = r"P_V(B) = \dfrac{3}{8}\times\dfrac{8}{5}"
        probaBcondV03 = r"P_V(B) = \dfrac{3}{5}"
        pBcondVs = [probaBcondV00, probaBcondV01, probaBcondV02, probaBcondV03]
        pBcondV = [MathTex(p) for p in pBcondVs]
        self.play(
            ReplacementTransform(full_proba_tree, pBcondV[0].next_to(q4, DOWN)),
        )
        self.wait()
        for i in range(len(pBcondV) - 1):
            self.play(
                ReplacementTransform(pBcondV[i], pBcondV[i+1].next_to(q4, DOWN))
            )
            self.wait()

        box_res = SurroundingRectangle(pBcondV[-1])
        self.play(Write(box_res))
        self.wait()
        
class ForeignCenterExo1Question5(Scene):
    def construct(self):
        msg1 = "Bac 2023 centres étrangers groupe 1 sujet 2"
        title1 = Title(f"{msg1}")
        self.add(title1.scale(1))
        self.wait(2)
        
        question5 = Title("Question 5 : Algorithmique")
        self.play(
            ReplacementTransform(title1, question5)
        )
        self.wait()
        

        q1_txt = r"On pose "
        q1_txt += r"\(S = 1 + \frac{1}{2} + \frac{1}{3} + \frac{1}{4}\dots\frac{1}{100}\)."
        q1 = Tex(q1_txt).scale(0.75)

        q12_txt = r"Parmi les scripts Python ci-dessous, celui qui permet "
        q12_txt += r"de calculer la somme \(S\) est : "
        q12 = Tex(q12_txt).next_to(q1, DOWN).scale(0.75)

        intro = VGroup(q1, q12).next_to(question5, DOWN)

        self.play(Write(intro))
        self.wait()
        
        code_a = """a.
def somme_a():
    S = 0
    for k in range(100):
        S = 1 / (k + 1)
    return S
"""        
        a = Code(
            code=code_a,
            tab_width=4,
            background="window",
            language="Python",
            font="Monospace"
        )
        
        code_b = """b.
def somme_b(): 
    S = 0
    for k in range(100):
        S = S + 1 / (k + 1)
    return S
"""        
        b =  Code(
            code=code_b,
            tab_width=4,
            background="window",
            language="Python",
            font="Monospace"
        )
        
        code_c = """c.
def somme_c():
    k = 0
    while S < 100:
        S = S + 1 / (k + 1)
    return S
"""
    
        c =  Code(
            code=code_c,
            tab_width=4,
            background="window",
            language="Python",
            font="Monospace"
        )
        
        code_d = """d.
def somme_d():
    k = 0
    while k < 100:
        S = S + 1 / (k + 1)
    return S
"""
   
        d =  Code(
            code=code_d,
            tab_width=4,
            background="window",
            language="Python",
            font="Monospace"
        )
        
        m1 = MobjectMatrix(
            [[a, b], [c, d]],
            v_buff=4.25,
            h_buff=10,
            left_bracket="\{",
            right_bracket="\}"
        ).next_to(intro, DOWN).scale(0.55)
        

        self.play(
            m1.animate.shift(1.95 * UP)
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
        
        solution1 = Title("Réponse b.")
        ent = m1.get_entries()
        sol_b = ent[1]
        box_b = SurroundingRectangle(sol_b)
        self.play(
            ReplacementTransform(attention_rep, solution1),
            Write(box_b)
        )
        self.wait()

        explanation = Title("Explications")

        code_a = """a.
def somme_a():
    S = 0
    for k in range(100):
        S = 1 / (k + 1)
    return S
"""        
        a = Code(
            code=code_a,
            tab_width=4,
            background="window",
            language="Python",
            font="Monospace"
        )
        
        
        box_a_false = SurroundingRectangle(a, color=RED)
        wrong_a = VGroup(a, box_a_false)
        self.play(
            FadeOut(box_b),
            ReplacementTransform(solution1, explanation),
            ReplacementTransform(m1, wrong_a.next_to(intro, DOWN))
        )
        self.wait()

        awrong = r"Dans le script a. la variable \(S\) "
        awrong += r"stocke les inverses mais ne les "
        awrong += r"ajoute pas."
        awrong += r"Résultat, le script renvoie \(S = 1\)."
        a_false = Tex(awrong).scale(0.75)
        self.play(
            Write(a_false.next_to(wrong_a, DOWN)),
        )
        self.wait()

        code_c = """c.
def somme_c():
    k = 0
    while S < 100:
        S = S + 1 / (k + 1)
    return S
"""
    
        c =  Code(
            code=code_c,
            tab_width=4,
            background="window",
            language="Python",
            font="Monospace"
        )

        box_c_false = SurroundingRectangle(c, color=RED)
        wrong_c = VGroup(c, box_c_false)
        cwrong = r"Dans le script c. la variable \(S\) "
        cwrong += r"stocke la somme des inverses de \((k + 1)\) "
        cwrong += r"mais la variable \(k\) ne change pas. "
        cwrong += r"Résultat, le script renvoie \(S = 100\)."
        c_false = Tex(cwrong).scale(0.75)
        self.play(
            ReplacementTransform(wrong_a, wrong_c),
            ReplacementTransform(a_false, c_false.next_to(wrong_c, DOWN)),
        )
        self.wait()
        c_block = VGroup(wrong_c, c_false)
        self.play(
            c_block.animate.shift(0.75 * DOWN)
        )
        self.wait()
        
        code_d = """d.
def somme_d():
    k = 0
    while k < 100:
        S = S + 1 / (k + 1)
    return S
"""
   
        d =  Code(
            code=code_d,
            tab_width=4,
            background="window",
            language="Python",
            font="Monospace"
        )

        box_d_false = SurroundingRectangle(d, color=RED)
        wrong_d = VGroup(d, box_d_false)
        dwrong = r"Dans le script d. la boucle \(while\) "
        dwrong += r"est conditionnée par la variable \(k\). "
        dwrong += r"Mais la variable \(k\) ne change pas. "
        dwrong += r"Résultat, le script tombe dans une boucle infinie."
        d_false = Tex(dwrong).scale(0.75)
        self.play(
            ReplacementTransform(wrong_c, wrong_d),
            ReplacementTransform(c_false, d_false.next_to(wrong_d, DOWN)),
        )
        self.wait()
        d_block = VGroup(wrong_d, d_false)
        self.play(
            d_block.animate.shift(0.75 * DOWN)
        )
        self.wait()
        
        b =  Code(
            code=code_b,
            tab_width=4,
            background="window",
            language="Python",
            font="Monospace"
        )
        
        code_b = """b.
def somme_b(): 
    S = 0
    for k in range(100):
        S = S + 1 / (k + 1)
    return S
"""
        box_b_true = SurroundingRectangle(b, color=GREEN)
        right_b = VGroup(b, box_b_true)
        bright = r"Dans le script b. la boucle \(for\) "
        bright += r"assure que la variable \(k\) prendra "
        bright += r"toutes les valeurs entières de \(0\) "
        bright += r"à 99. Comme la variable \(S\) ajoute "
        bright += r"bien la somme des inverses, le script "
        bright += r"renvoie bien le bon résultat."
        b_true = Tex(bright).scale(0.65)
        self.play(
            ReplacementTransform(wrong_d, right_b),
            ReplacementTransform(d_false, b_true.next_to(right_b, DOWN)),
        )
        self.wait()
        b_block = VGroup(right_b, b_true)
        self.play(
            b_block.animate.shift(0.75 * DOWN)
        )
        self.wait()


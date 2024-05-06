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
# Asie 23 mars 2023 Sujet 1
##################################################

# Exo 4
class AsiaExo1Question1(Scene):
    def construct(self):
        msg1 = "Bac Asie 23 mars 2023 Sujet 1 Exercice 4"
        title1 = Title(f"{msg1}")
        self.add(title1.scale(1))
        self.wait(2)

        intro = Paragraph(
            "Une urne contient 15 billes indiscernables au toucher, numérotées de 1 à 15.",
            "La bille numérotée 1 est rouge.",
            "Les billes numérotées 2 à 5 sont bleues.",
            "Les autres billes sont vertes.",
            " ",
            "On choisit une bille au hasard dans l'urne.",
            "On note R (respectivement B et V) l'événement :",
            "\"La bille tirée est rouge\" (respectivement bleue et verte)."
            )
        self.play(
            Write(intro.scale(0.65))
        )
        self.wait(4)
        question1 = Title("Question 1")
        q1_txt = r"Quelle est la probabilité que la bille tirée soit blueue "
        q1_txt += r"ou numérotée d'un nombre pair ?"
        q1 = Tex(q1_txt).next_to(question1, 0.5*DOWN).scale(0.85)
        rep1 = Table(
            [
                [
                    "Réponse A",
                    "Réponse B",
                    "Réponse C",
                    "Réponse D"
                ],
                [
                    "7/15",
                    "9/15",
                    "11/10",
                    "Aucune des\naffirmations\nprécédentes\nn'est juste."
                ]
            ]
        ).next_to(q1, DOWN).scale(0.75)
        block1 = VGroup(q1, rep1)
        self.play(
            ReplacementTransform(title1, question1),
            ReplacementTransform(intro, block1)
        )
        self.wait(4)
        

#         q1_txt = r"Soit \(f\) la fonction définie sur \(\mathbb{R}\) par "
#         q1_txt += r"\(f(x) = xe^x\)."
#         q1 = Tex(q1_txt).scale(0.75)

#         q1_txt2 = r"Une primitive \(F\) sur \(\mathbb{R}\) de la fonction "
#         q1_txt2 += r"\(f\) est définie par :"
#         q1_q = Tex(q1_txt2).next_to(q1, DOWN).scale(0.75)

#         a = Tex(r"A.\(F(x) = \dfrac{x^2}{2}e^x\)")
#         b = Tex(r"B.\(F(x) = (x - 1)e^x\)")
#         c = Tex(r"C.\(F(x) = (x + 1)e^x\)")
#         d = Tex(r"D.\(F(x) = \dfrac{2}{x}e^{x^2}\)")
        
#         m1 = MobjectMatrix(
#             [[a, b], [c, d]],
#             v_buff=2.5,
#             h_buff=5,
#             left_bracket="\{",
#             right_bracket="\}"
#         ).next_to(q1_q, DOWN).scale(0.75)
        
#         mobj1 = VGroup(q1, q1_q, m1)


#         self.play(
#             Write(mobj1.next_to(title1, 1.75 * DOWN))
#         )
#         self.wait(4)

#         noter = Title("Mettez pause pour noter la question")
#         self.play(
#             ReplacementTransform(question1, noter)
#         )
#         self.wait(4)

#         attention_rep = Title("Cherchez avant de regarder le corrigé")
#         self.play(
#             ReplacementTransform(noter, attention_rep)
#         )
#         self.wait(4)

#         ent = m1.get_entries()
#         sol_B = ent[1]
#         box_B = SurroundingRectangle(sol_B)
#         solution1 = Title("Réponse B")
#         self.play(
#             ReplacementTransform(attention_rep, solution1),
#             Write(box_B)
#         )
#         self.wait()
        
#         r1 = r"Rappel : \( (uv)' = u'v + uv'\)"
#         r12 = r"Pour \(F(x) = (x-1)e^x\) posons \(u = x - 1\) et \(v = e^x\)"
#         r13 = r"Ainsi \(u' = 1\) et \(v' = e^x\)"
#         r14 = r"D'où \(F'(x) = e^x + (x - 1)e^x = e^x + xe^x - e^x\)"
#         r15 = r"Finalement \(F'(x) = xe^x = f(x)\) CQFD"
        
#         rep = [r1, r12, r13, r14, r15]
#         p = [Tex(r) for r in rep]

#         explanation = Title("Explications")
#         self.play(
#             Unwrite(box_B),
#             ReplacementTransform(solution1, explanation),
#             ReplacementTransform(mobj1, p[0].next_to(title1, 2 * DOWN))
#         )
#         self.wait()

#         for i in range(1, len(p)):
#             self.play(Write(p[i].next_to(p[i-1], DOWN)))
#             self.wait(2)
        

        

# class AsiaExo1Question2(Scene):
#     def construct(self):
#         msg1 = "Bac Asie 23 mars 2023 Sujet 1"
#         title1 = Title(f"{msg1}")
#         self.add(title1.scale(1))
#         self.wait(2)
        
#         question2 = Title("Question 2 : Dérivées d'une fonction")
#         self.play(
#             ReplacementTransform(title1, question2)
#         )
#         self.wait()
        

#         q1_txt = r"La courbe \(\mathcal{C}\) ci-dessous représente une "
#         q1_txt += r"fonction \(f\) définie et deux fois dérivable "
#         q1_txt += r"sur \(]0;+\infty[\). On sait que :"
#         q1 = Tex(q1_txt).scale(0.75)

#         q12 = r"\(\bullet\) le maximum de la fonction \(f\) est atteint "
#         q12 += r"au point d'abscisse 3 ;"
#         q1_q = Tex(q12).next_to(q1, DOWN).scale(0.7)
#         q12bis = r"\(\bullet\) le point P d'abscisse 5 est l'unique point "
#         q12bis += r"d'inflexion de la courbe \(\mathcal{C}\)."
#         q1_qbis = Tex(q12bis).next_to(q1_q, DOWN).scale(0.7)

#         mobj1 = VGroup(q1, q1_q, q1_qbis)
#         self.play(Write(mobj1.next_to(title1, 0.25 * DOWN)))
#         self.wait(2)
        
#         ax = Axes(
#             x_range=[0, 10, 1],
#             y_range=[-2, 6, 1],
#             x_axis_config={"numbers_to_include": np.arange(0, 10, 1)},
#             y_axis_config={"numbers_to_include": np.arange(-2, 6, 1)},
#         ).add_coordinates().scale(0.8)


#         def func(x):
#             return (x - 1) * e ** (2.31 - 0.5 * x)
#         graph = ax.plot(
#             func,
#             x_range=[0.7, 10, 1],
#             color=MAROON
#         )

        
#         tan_x_3 = ax.plot(lambda x: 4.5, x_range=[1, 5, 1], color=YELLOW)
#         tan_x_5 = ax.plot(
#             lambda x: (-3.25/4)*x + 29.25/4,
#             x_range=[2, 9, 1], color=YELLOW
#         )
        
#         A = Dot(ax.coords_to_point(3, 4.5), color=GREEN)
#         A_lines = ax.get_lines_to_point(ax.c2p(3, 4.5), color=GREEN)
#         P = Dot(ax.coords_to_point(5, 3.25), color=GREEN)
#         P_lines = ax.get_lines_to_point(ax.c2p(5, 3.25), color=GREEN)
#         P_label = Text("P").next_to(P, 0.5*UR).scale(0.7).set_color(GREEN)

#         mobj2 = VGroup(
#             ax, graph, A, A_lines, tan_x_3, P, P_lines, P_label, tan_x_5
#         )
#         self.play(Write(mobj2.next_to(mobj1, 0.25 * DOWN)))
#         self.wait(5)

        
#         q1a = Tex(r"On a :").scale(0.75)
#         repA11 = r"A. Pour tout \(x\in]0;5[\), "
#         a11 = Tex(repA11)
#         repA21 = r"\(f(x)\) et \(f'(x)\) sont de même signe"
#         a21 = Tex(repA21)
#         repB12 = r"B. Pour tout \(x\in]5;+\infty[\), "
#         b12 = Tex(repB12)
#         repB22 = r"\(f(x)\) et \(f'(x)\) sont de même signe"
#         b22 = Tex(repB22)
#         repC31 = r"C. Pour tout \(x\in]0;5[\), "
#         c31 = Tex(repC31)
#         repC41 = r"\(f'(x)\) et \(f''(x)\) sont de même signe"
#         c41 = Tex(repC41)
#         repD32 = r"D. Pour tout \(x\in]5;+\infty[\), "
#         d32 = Tex(repD32)
#         repD42 = r"\(f(x)\) et \(f''(x)\) sont de même signe"
#         d42 = Tex(repD42)
        
#         m1 = MobjectMatrix(
#             [[a11, b12], [a21, b22], [c31, d32], [c41, d42]],
#             v_buff=0.85,
#             h_buff=10,
#             left_bracket="\{",
#             right_bracket="\}"
#         ).next_to(q1a, 0.25*DOWN).scale(0.75)
        
#         mobj3 = VGroup(q1a, m1)


#         self.play(
#             ReplacementTransform(mobj1, mobj3.next_to(mobj1, 3 * DOWN)),
#             # mobj2.animate.next_to(title1, 0.015*DOWN).scale(0.75)
#             mobj2.animate.shift(3 * UP).scale(0.7)
#         )
#         self.wait(4)

#         noter = Title("Mettez pause pour noter la question")
#         self.play(
#             ReplacementTransform(question2, noter)
#         )
#         self.wait(4)

#         attention_rep = Title("Cherchez avant de regarder le corrigé")
#         self.play(
#             ReplacementTransform(noter, attention_rep)
#         )
#         self.wait(4)

        
#         solution1 = Title("Réponse D")

#         # Version 1
#         ent = m1.get_entries()
#         sol_D1 = ent[5]
#         sol_D2 = ent[7]
#         sols_D = VGroup(sol_D1, sol_D2)

#         # Version 2
#         col1 = m1.get_columns()[1]
#         sols_D2 = col1[2:]
#         box_D = SurroundingRectangle(sols_D2)
        
#         self.play(
#             ReplacementTransform(attention_rep, solution1),
#             Write(box_D)
#         )
#         self.wait(4)

#         explanation = Title("Explications")
        
#         wrong_A = VGroup(ent[0], ent[2])
#         box_A = SurroundingRectangle(wrong_A, color=RED)
        
#         self.play(
#             ReplacementTransform(solution1, explanation),
#             ReplacementTransform(box_D, box_A),
#             mobj2.animate.shift(3.5 * LEFT),
#         )
#         self.wait(2)
#         awrong_dict = {
#             r"Pour tout \(x\in ]0;1], f(x)\leqslant 0\).": RED,
#             r"Alors que la courbe est croissante sur \(]0;1]\).": GREEN,
#             r"Donc \(f'(x) \geqslant 0\) sur \(]0;1]\).": GREEN,
#             r"Pour tout \(x\in ]0;1], f(x)f'(x)\leqslant 0\).": RED
#         }
#         a_proof = [
#             Tex(
#                 text,
#                 color=color
#             ).scale(0.75) for text, color in awrong_dict.items()
#         ]
#         self.play(
#             Write(
#                 a_proof[0].next_to(
#                     explanation,
#                     0.25 * DOWN
#                 )
#             )
#         )
#         self.wait(2)
#         for i in range(len(a_proof) - 1):
#             self.play(
#                 Write(a_proof[i + 1].next_to(a_proof[i], 0.75 * DOWN))
#             )
#             self.wait(2)
#         proofA = VGroup(*a_proof)
#         self.play(proofA.animate.shift(2.5 * RIGHT))
#         self.wait(4)

#         wrong_B = VGroup(ent[1], ent[3])
#         box_B = SurroundingRectangle(wrong_B, color=RED)
        
#         self.play(
#             ReplacementTransform(box_A, box_B),
#             FadeOut(proofA)
#         )
#         self.wait()
#         bwrong_dict = {
#             r"Pour tout \(x\in [5;+\infty[, f(x)\geqslant 0\).": GREEN,
#             r"Alors que la courbe est décroissante sur \([5;+\infty[\).": RED,
#             r"Donc \(f'(x) \leqslant 0\) sur \([5;+\infty[\).": RED,
#             r"Pour tout \(x\in [5;+\infty[, f(x)f'(x)\leqslant 0\).": RED
#         }
#         b_proof = [
#             Tex(
#                 text,
#                 color=color
#             ).scale(0.75) for text, color in bwrong_dict.items()
#         ]
#         self.play(
#             Write(
#                 b_proof[0].next_to(
#                     explanation,
#                     0.25 * DOWN
#                 )
#             )
#         )
#         self.wait(2)
#         for i in range(len(b_proof) - 1):
#             self.play(
#                 Write(b_proof[i + 1].next_to(b_proof[i], 0.75 * DOWN))
#             )
#             self.wait(2)
#         proofB = VGroup(*b_proof)
#         self.play(proofB.animate.shift(2.5 * RIGHT))
#         self.wait(4)


#         wrong_C = VGroup(ent[4], ent[6])
#         box_C = SurroundingRectangle(wrong_C, color=RED)
        
#         self.play(
#             ReplacementTransform(box_B, box_C),
#             FadeOut(proofB)
#         )
#         self.wait(2)
#         cwrong_dict = {
#             r"Pour tout \(x\in ]0;3], f'(x)\geqslant 0\).": GREEN,
#             r"Alors que la courbe est concave sur \(]0;3]\).": RED,
#             r"Donc \(f''(x) \leqslant 0\) sur \(]0;3]\).": RED,
#             r"Pour tout \(x\in ]0;3], f'(x)f''(x)\leqslant 0\).": RED
#         }
#         c_proof = [
#             Tex(
#                 text,
#                 color=color
#             ).scale(0.75) for text, color in cwrong_dict.items()
#         ]
#         self.play(
#             Write(
#                 c_proof[0].next_to(
#                     explanation,
#                     0.25 * DOWN
#                 )
#             )
#         )
#         self.wait(2)
#         for i in range(len(c_proof) - 1):
#             self.play(
#                 Write(c_proof[i + 1].next_to(c_proof[i], 0.75 * DOWN))
#             )
#             self.wait(2)
#         proofC = VGroup(*c_proof)
#         self.play(proofC.animate.shift(2.5 * RIGHT))
#         self.wait(4)

#         right_D = VGroup(ent[5], ent[7])
#         box_D = SurroundingRectangle(right_D, color=GREEN)
        
#         self.play(
#             ReplacementTransform(box_C, box_D),
#             FadeOut(proofC)
#         )
#         self.wait(2)
#         dwrong_dict = {
#             r"Pour tout \(x\in ]5;+\infty[, f(x)\geqslant 0\).": GREEN,
#             r"La courbe est convexe sur \(]5;+\infty[\).": GREEN,
#             r"Donc \(f''(x) \geqslant 0\) sur \(]5;+\infty[\).": GREEN,
#             r"Pour tout \(x\in ]5;+\infty[, f(x)f''(x)\geqslant 0\).": GREEN
#         }
#         d_proof = [
#             Tex(
#                 text,
#                 color=color
#             ).scale(0.75) for text, color in dwrong_dict.items()
#         ]
#         self.play(
#             Write(
#                 d_proof[0].next_to(
#                     explanation,
#                     0.25 * DOWN
#                 )
#             )
#         )
#         self.wait(2)
#         for i in range(len(d_proof) - 1):
#             self.play(
#                 Write(d_proof[i + 1].next_to(d_proof[i], 0.75 * DOWN))
#             )
#             self.wait(2)
#         proofD = VGroup(*d_proof)
#         self.play(proofD.animate.shift(2.5 * RIGHT))
#         self.wait(4)

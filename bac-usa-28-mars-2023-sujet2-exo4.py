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
            self.wait(2)
            for i in range(len(calcs) - 1):
                self.play(
                    ReplacementTransform(
                        calcs[i],
                        calcs[i+1].next_to(next2obj, direction)
                    )
                )
                self.wait(2)

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
            self.wait(2)
            for i in range(len(tex_list) - 1):
                self.play(
                    Write(
                        tex_list[i+1].next_to(tex_list[i], direction)
                    )
                )
                self.wait(2)
                
##################################################
# USA 28 mars 2023 Sujet 2
##################################################

# Exo 4 Question 1
class USAExo4Question1(Scene):
    def construct(self):
        msg1 = "Bac USA 28 mars 2023 Sujet 2 Exercice 4"
        title1 = Title(f"{msg1}")
        self.add(title1.scale(1))
        self.wait(2)

        
        question1 = Title("Question 1")
        q1_txt = [
            r"1. On considère la fonction \(f\) définie sur l'intervalle \(]1;+\infty[\) par",
            r"\(f(x) = 0,05 - \dfrac{\ln(x)}{x - 1}\).",
            r"La limite de la fonction \(f\) en \(+\infty\) est égale à : "
        ]
        q1 = [Tex(t) for t in q1_txt]
        
        disp_tex_list(self, 
            previous_mobj=None,
            tex_list=q1,
            next2obj=title1,
            direction=DOWN
        )
        a = r"a. \(+\infty\)"
        b = r"b. 0,05"
        c = r"c. \(-\infty\)"
        d = r"d. 0"
        m1 = MobjectMatrix(
            [[Tex(a), Tex(b)], [Tex(c), Tex(d)]],
            v_buff=2.5,
            h_buff=8,
            left_bracket="\{",
            right_bracket="\}"
        ).scale(0.75)

        
        self.play(
            ReplacementTransform(title1, question1),
            Write(m1.next_to(q1[-1], DOWN))
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
        sol_b = ent[1]
        box_b = SurroundingRectangle(sol_b)
        solution1 = Title("Réponse b")
        self.play(
            ReplacementTransform(attention_rep, solution1),
            Write(box_b)
        )
        self.wait()

        
        explanation = Title("Explications")

        self.play(
            Unwrite(box_b),
            ReplacementTransform(solution1, explanation)
        )
        self.wait()
        
        B00 = r"Par croissance comparée \(\lim_{x\to +\infty}\dfrac{\ln(x)}{x} = 0\)"
        B01 = r"\(x\) et \(x-1\) sont équivalents en l'infini."
        B02 = r"Pour les sceptiques, factorisons \(\dfrac{\ln(x)}{x - 1} = \dfrac{\ln(x)}{x\left(1 - \dfrac{1}{x}\right)}\)"
        B03 = r"Ainsi \(\dfrac{\ln(x)}{x - 1} = \dfrac{\ln(x)}{x}\times \dfrac{1}{1 - \dfrac{1}{x}}\)"
        B04 = r"Et \(\dfrac{1}{1 - \dfrac{1}{x}}\) tend vers 1 car \(\dfrac{1}{x}\) tend vers zéro."
        B05 = r"D'où le résultat \(\lim_{x\to +\infty}0,05 - \dfrac{\ln(x)}{x - 1} = 0,05\)"
        
        B = [B00, B01, B02, B03, B04, B05]
        dB = [Tex(d).scale(0.75) for d in B]

        

        disp_calculations(self, 
            previous_mobj=m1,
            calcs=dB,
            next2obj=q1[-1],
            direction=DOWN
        )
        


# Question 2
class USAExo4Question2(Scene):
    def construct(self):
        msg1 = "Bac USA 28 mars 2023 Sujet 2 Exercice 4"
        title2 = Title(f"{msg1}")
        self.add(title2.scale(1))
        self.wait(2)

        q2_txt = [
            r"2. On considère une fonction \(h\) continue sur l'intervalle [-2;4] telle que : ",
            r"\(h(-1) = 0,\quad h(1) = 4,\quad h(3) = -1\).",
            r"On peut affirmer que : "
        ]
        q2 = [Tex(t).scale(0.65) for t in q2_txt]
        
        disp_tex_list(self, 
            previous_mobj=None,
            tex_list=q2,
            next2obj=title2,
            direction=DOWN
        )

        question2 = Title("Question 2")

        a = r"a. la fonction \(h\) est croissante sur l'intervalle [-1; 1]."
        b = r"b. la fonction \(h\) est positive sur l'intervalle [-1; 1]."
        c = r"c. il existe au moins un réel \(a\) dans l'intervalle [1;3] tel que \(h(a) = 1\)."
        d = r"d. l'équation \(h(x) = 1\) admet exactement 2 solutions dans l'intervalle [-2 ; 4]."
        m1 = MobjectMatrix(
            [
                [Tex(a).scale(0.65)],
                [Tex(b).scale(0.65)],
                [Tex(c).scale(0.65)],
                [Tex(d).scale(0.65)]
            ],
            v_buff=1,
            h_buff=8,
            left_bracket="\{",
            right_bracket="\}"
        ).scale(0.85)

        
        
        self.play(
            ReplacementTransform(title2, question2),
            Write(m1.next_to(q2[-1], DOWN))
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

        
        a_w00 = r"Soit \(h(x) = \dfrac{5}{8}x^3 - 3x^2 + \dfrac{11}{8}x + 5\)"
        a_w01 = r"On a bien \(h(-1) = 0, h(1) = 4, h(3) = -1\)."
        a_w02 = r"Mais \(h(0) = 5 > h(1)\) donc \(h\) n'est pas croissante."
        a_w03 = r"\(h\) n'est pas croissante sur [-1;1]."

        a_w = [a_w00, a_w01, a_w02, a_w03]
        a_wr = [Tex(d).scale(0.75) for d in a_w]

        disp_calculations(self, 
            previous_mobj=None,
            calcs=a_wr,
            next2obj=m1,
            direction=DOWN
        )

        wrong_b = VGroup(ent[1])
        box_b = SurroundingRectangle(wrong_b, color=RED)
        
        self.play(
            ReplacementTransform(box_a, box_b),
        )
        self.wait(2)


        b_w00 = r"Soit \(h(x) = -\dfrac{41}{24}x^3 + 4x^2 + \dfrac{89}{24}x - 2\)"
        b_w01 = r"On a bien \(h(-1) = 0, h(1) = 4, h(3) = -1\)."
        b_w02 = r"Mais \(h(0) = -2\) donc \(h\) n'est pas positive."
        b_w03 = r"\(h\) n'est pas positive sur [-1;1]."

        b_w = [b_w00, b_w01, b_w02, b_w03]
        b_wr = [Tex(d).scale(0.75) for d in b_w]

        disp_calculations(self, 
            previous_mobj=a_wr[-1],
            calcs=b_wr,
            next2obj=m1,
            direction=DOWN
        )

        wrong_d = VGroup(ent[3])
        box_d = SurroundingRectangle(wrong_d, color=RED)
        
        self.play(
            ReplacementTransform(box_b, box_d),
        )
        self.wait(2)

        
        
        D00 = r"Soit \(h(x) = \dfrac{x}{120}(-37x^3 - 14x^2 + 277x + 254)\)"
        D01 = r"On a bien \(h(-1) = 0, h(1) = 4, h(3) = -1\)."
        D02 = r"De plus \(h(-2) = 1\) et \(h\) est bien continue."
        D03 = r"En utilisant le théorème des valeurs intermédiaires (TVI),"
        D04 = r"sur l'intervalle [-1;1] puis sur [1; 3],"
        D05 = r"on obtient au moins deux antécédents de 1 par \(h\)."
        D06 = r"On a donc au moins trois antécédents pour 1 par \(h\)."
        
        d_w = [D00, D01, D02, D03, D04, D05, D06]
        d_wr = [Tex(d).scale(0.75) for d in d_w]

        disp_calculations(self, 
            previous_mobj=b_wr[-1],
            calcs=d_wr,
            next2obj=m1,
            direction=DOWN
        )

        right_c = VGroup(ent[2])
        box_c = SurroundingRectangle(right_c, color=GREEN)
        
        self.play(
            ReplacementTransform(box_d, box_c),
        )
        self.wait(2)

        
        C00 = r"Par hypothèses \(h\) est continue sur [-2;4]."
        C01 = r"Donc \(h\) est continue sur \([1; 3]\subset [-2;4]\)."
        C02 = r"Or \(h(1) = 4 > 1\) et \(h(3) = -1 < 1\)."
        C03 = r"D'après le théorème des valeurs intermédiaires (TVI), "
        C04 = r"il existe au moins un nombre réel \(a\) sur [1;3] tel que \(h(a) = 1\)."
        
        C_r = [C00, C01, C02, C03, C04]
        C_right = [Tex(d).scale(0.75) for d in C_r]

        disp_calculations(self, 
            previous_mobj=d_wr[-1],
            calcs=C_right,
            next2obj=m1,
            direction=DOWN
        )

        

# Question 3
class USAExo4Question3(Scene):
    def construct(self):
        msg1 = "Bac USA 28 mars 2023 Sujet 2 Exercice 4"
        title3 = Title(f"{msg1}")
        self.add(title3.scale(1))
        self.wait(2)


        question3 = Title("Question 3").scale(0.75)
        q3_txt = [
            r"2. On considère deux suites \((u_n)\) et \((v_n)\) à termes strictement positifs telles que ",
            r"\(\lim_{n\to +\infty}u_n = +\infty\) et \((v_n)\) converge vers 0.",
            r"On peut affirmer que : "
        ]
        q3 = [Tex(t).scale(0.75) for t in q3_txt]
        
        disp_tex_list(self, 
            previous_mobj=None,
            tex_list=q3,
            next2obj=title3,
            direction=DOWN
        )

        
        a = r"a. la suite \(\left(\dfrac{1}{v_n}\right)\) converge."
        b = r"b. la suite \(\left(\dfrac{v_n}{u_n}\right)\) converge."
        c = r"c. la suite \((u_n)\) est croissante."
        d = r"d. \(\lim_{n\to +\infty}(-u_n)^n = -\infty\)"
        
        m1 = MobjectMatrix(
            [[Tex(a), Tex(b)], [Tex(c), Tex(d)]],
            v_buff=1.5,
            h_buff=8,
            left_bracket="\{",
            right_bracket="\}"
        ).scale(0.85)

        
        self.play(
            ReplacementTransform(title3, question3),
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

        
        aWR00 = r"Puisque \((v_n)\) converge vers 0 alors son inverse diverge."
        aWR01 = r"En effet, \(\lim_{x\to 0}\dfrac{1}{x} = \infty\)"
        
        aWR = [aWR00, aWR01]
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

        
        cWR00 = r"Considérer la suite à termes strictement positifs \(u_n = n + 2 + (-1)^n\)"
        cWR01 = r"\(u_0 = 1, u_1 = 2, u_2 = 5, u_3 = 4\) la suite n'est pas croissante."
        cWR02 = r"Pourtant \(\lim_{n\to +\infty}u_n = +\infty\)."

        
        cWR = [cWR00, cWR01, cWR02]
        cWRg = [Tex(d).scale(0.75) for d in cWR]

        disp_calculations(self, 
            previous_mobj=aWRg[-1],
            calcs=cWRg,
            next2obj=m1,
            direction=DOWN
            )
        
        
        
        wrong_d = VGroup(ent[3])
        box_d = SurroundingRectangle(wrong_d, color=RED)
        
        self.play(
            ReplacementTransform(box_c, box_d),
        )
        self.wait(2)

        
        dWR00 = r"La suite \((-u_n)^n = (-1)^nu_n\) est alternée."
        dWR01 = r"Elle diverge sans atteindre de limite particulière."
        dWR02 = r"Pour \(n\) pair ça monte et pour \(n\) impair ça descend."
        
        dWR = [dWR00, dWR01, dWR02]
        dWRg = [Tex(d).scale(0.75) for d in dWR]

        disp_calculations(self, 
            previous_mobj=cWRg[-1],
            calcs=dWRg,
            next2obj=m1,
            direction=DOWN
            )
        
        

        right_b = VGroup(ent[1])
        box_b = SurroundingRectangle(right_b, color=GREEN)
        
        self.play(
            ReplacementTransform(box_d, box_b),            
        )
        self.wait(2)

        
        B00 = r"Puisque \(\lim_{n\to +\infty}u_n = +\infty\) alors "
        B01 = r"on a \(\lim_{n\to +\infty}\dfrac{1}{u_n} = 0\)."
        B02 = r"Or \(\lim_{n\to +\infty}v_n = 0\)"
        B03 = r"Donc \(\lim_{n\to +\infty}\dfrac{v_n}{u_n} = 0\)"
        
        B = [B00, B01, B02, B03]
        Br = [Tex(d).scale(0.75) for d in B]

        disp_calculations(self, 
            previous_mobj=dWRg[-1],
            calcs=Br,
            next2obj=m1,
            direction=DOWN
        )



# Question 4
class USAExo4Question4(Scene):
    def construct(self):
        msg1 = "Bac USA 28 mars 2023 Sujet 2 Exercice 4"
        title4 = Title(f"{msg1}")
        self.add(title4.scale(1))
        self.wait(2)

        
        question4 = Title("Question 4").scale(0.85)
        q4_txt = [
            r"4. Pour participer à un jeu, un joueur doit payer 4€.",
            r"Il lance ensuite un dé équilibré à six faces : ",
            r"\(\bullet\) s'il obtient 1, il remporte 12€ ;",
            r"\(\bullet\) s'il obtient un nombre pair, il remporte 3€ ;",
            r"\(\bullet\) sinon, il ne remporte rien.",
            r"En moyenne, le joueur : "
        ]
        q4 = [Tex(r).scale(0.65) for r in q4_txt]

        disp_tex_list(self, 
            previous_mobj=None,
            tex_list=q4,
            next2obj=title4,
            direction=DOWN
        )
        
        a = r"a. gagne 3,50€"
        b = r"b. perd 3€"
        c = r"c. perd 1,50€"
        d = r"d. perd 0,50€"
        
        m1 = MobjectMatrix(
            [
                [Tex(a), Tex(b)],
                [Tex(c), Tex(d)],
            ],
            v_buff=1.5,
            h_buff=8,
            left_bracket="\{",
            right_bracket="\}"
        ).scale(0.85)

        
        self.play(
            ReplacementTransform(title4, question4),
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
        sol_d = ent[3]
        box_d = SurroundingRectangle(sol_d)
        solution4 = Title("Réponse d")
        self.play(
            ReplacementTransform(attention_rep, solution4),
            Write(box_d)
        )
        self.wait()

        
        explanation = Title("Explications")

        dRight00 = r"Soit \(X\) la variable aléatoire indiquant le gain du joueur."
        dRight01 = r"Les valeurs possibles pour \(X\) sont : \(\{8, -1, -4\}\)."
        dRight02 = r"En effet, dans tous les cas il doit payer la partie."
        dRight03 = r"Les probabilités associées sont : \(\left\{\dfrac{1}{6}, \dfrac{3}{6}, \dfrac{2}{6}\right\}\)."
        dRight04 = r"D'où l'espérance de gain : "
        dRight05 = r"\(E(X) = \dfrac{1}{6}(8\times 1 - 1\times 3 - 4\times 2)\)"
        dRight06 = r"Finalement, \(E(X) = -\dfrac{3}{6} = -0,50\)"
        
        dRight = [
            dRight00,
            dRight01,
            dRight02,
            dRight03,
            dRight04,
            dRight05,
            dRight06
        ]
        Cr = [Tex(r).scale(0.65) for r in dRight]
        disp_calculations(self, 
            previous_mobj=None,
            calcs=Cr,
            next2obj=m1,
            direction=DOWN
            )



# Question 5
class USAExo4Question5(Scene):
    def construct(self):
        msg1 = "Bac USA 28 mars 2023 Sujet 2 Exercice 4"
        title5 = Title(f"{msg1}")
        self.add(title5.scale(1))
        self.wait(2)

        

        question5 = Title("Question 5").scale(0.55)
        q5_00 = r"5. On considère variable aléatoire \(X\) "
        q5_00 += r"suivant la loi binomiale \(\mathcal{B}(3; p)\)."
        q5_01 = r"On sait que \(P(X = 0) = \dfrac{1}{125}.\)"
        q5_02 = r"On peut affirmer que : "
        q5_txt = [q5_00, q5_01, q5_02]
        q5 = [Tex(r).scale(0.55) for r in q5_txt]

        disp_tex_list(self, 
            previous_mobj=None,
            tex_list=q5,
            next2obj=title5,
            direction=DOWN
        )
        
        a = r"a. \(p = \dfrac{1}{5}\)"
        b = r"b. \(P(X = 1) = \dfrac{124}{125}\)"
        c = r"c. \(p = \dfrac{4}{5}\)"
        d = r"d. \(P(X = 1) = \dfrac{4}{5}\)"
        
        m1 = MobjectMatrix(
            [
                [Tex(a), Tex(b)],
                [Tex(c), Tex(d)],
            ],
            v_buff=2.25,
            h_buff=8,
            left_bracket="\{",
            right_bracket="\}"
        ).scale(0.85)

        
        self.play(
            ReplacementTransform(title5, question5),
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
        sol_a = ent[0]
        box_a = SurroundingRectangle(sol_a)
        solution5 = Title("Réponse a")
        self.play(
            ReplacementTransform(attention_rep, solution5),
            Write(box_a)
        )
        self.wait()

        
        explanation = Title("Explications")
        self.play(ReplacementTransform(solution5, explanation))
        self.wait()
        
        aRight00 = r"Puisqu'il y a 3 tirages alors \(P(X = 0) = p^3\)"
        aRight01 = r"On en déduit que \(p = \dfrac{1}{5}\)."

        aRight = [aRight00, aRight01]
        Ar = [Tex(r).scale(0.6) for r in aRight]
        disp_calculations(self, 
            previous_mobj=None,
            calcs=Ar,
            next2obj=m1,
            direction=DOWN
            )


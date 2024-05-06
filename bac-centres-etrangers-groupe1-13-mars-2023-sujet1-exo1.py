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
# Centres étrangers Groupe 1 Sujet 1
##################################################

# Exo 1
class ForeignCenterExo1Question1(Scene):
    def construct(self):
        msg1 = "Bac 2023 centres étrangers groupe 1 sujet 1"
        title1 = Title(f"{msg1}")
        self.add(title1.scale(1))
        self.wait(2)
        
        question1 = Title("Question 1 : Convergence d'une suite")
        self.play(
            ReplacementTransform(title1, question1)
        )
        self.wait()
        

        q1_txt = r"On considère la suite numérique \((u_n)\) définie pour "
        q1_txt += r"tout \(n\) entier naturel par "
        q1_txt += r"\[u_n = \dfrac{1 + 2^n}{3 + 5^n}\]"
        q1 = Tex(q1_txt).scale(0.75)

        q1_q = Tex("Cette suite : ").next_to(q1, DOWN).scale(0.75)

        a = Tex(r"a. diverge vers \(+\infty\)")
        c = Tex(r"c. converge vers \(0\)")
        b = Tex(r"b. converge vers \(\dfrac{2}{5}\)")
        d = Tex(r"d. converge vers \(\dfrac{1}{3}\)")
        
        m1 = MobjectMatrix(
            [[a, c], [b, d]],
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
        
        solution1 = Title("Réponse c")

        r1 = r"u_n = \dfrac{1 + 2^n}{3 + 5^n}"
        r12 = r"u_n = \dfrac{2^n\left(\frac{1}{2^n} + 1\right)}{5^n\left(\frac{3}{5^n} + 1\right)}"
        r13 = r"u_n = \dfrac{2^n}{5^n}\dfrac{\frac{1}{2^n} + 1}{\frac{3}{5^n} + 1}"
        r14 = r"u_n = \left(\dfrac{2}{5}\right)^n\dfrac{\left(\frac{1}{2}\right)^n + 1}{\left(\frac{3}{5}\right)^n + 1}"
        
        rep = [r1, r12, r13, r14]
        p = [MathTex(r) for r in rep]
        
        self.play(
            ReplacementTransform(attention_rep, solution1),
            ReplacementTransform(mobj1, p[0].next_to(title1, 2 * DOWN))
        )
        self.wait()

        for i in range(1, len(p)):
            self.play(Write(p[i].next_to(p[i-1], DOWN)))
            self.wait(2)
        

        l1 = r"\vert q \vert < 1\Rightarrow \lim_{n\to\infty}q^n = 0"
        l1m = MathTex(l1).next_to(solution1, 2 * DOWN)

        l2 = r"q\in\left\{\dfrac{2}{5}, \dfrac{1}{2}, \dfrac{3}{5}\right\}"
        l2 += r"\Rightarrow \lim_{n\to\infty}q^n = 0"
        l2m = MathTex(l2).next_to(l1m, DOWN)

        l3 = r"\lim_{n\to\infty}1 + \left(\dfrac{1}{2}\right)^n = "
        l3 += r"\lim_{n\to\infty}1 + \left(\dfrac{3}{5}\right)^n = "
        l3 += r"1"
        l3m = MathTex(l3).next_to(l2m, DOWN)

        l4 = r"\lim_{n\to\infty}u_n = 0\times 1 = 0"
        l4m = MathTex(l4).next_to(l3m, DOWN)

        l = [l1m, l2m, l3m, l4m]
        
        self.play(
            *[ReplacementTransform(p[i], l[i]) for i in range(len(l))]
        )
        self.wait(3)

        mobj1 = VGroup(l1m, l2m, l3m, l4m)

        final = r"\lim_{n\to\infty}u_n = \lim_{n\to\infty} "
        final += r"\dfrac{1 + 2^n}{3 + 5^n} = 0"
        m_final = MathTex(final)
        box_final = SurroundingRectangle(m_final)

        mobj2 = VGroup(m_final, box_final)

        self.play(
            ReplacementTransform(
                mobj1,
                mobj2.next_to(solution1, 2 * DOWN)
            )
        )
        self.wait(4)


class ForeignCenterExo1Question2(Scene):
    def construct(self):
        msg1 = "Bac 2023 centres étrangers groupe 1 sujet 1"
        title1 = Title(f"{msg1}")
        self.add(title1.scale(1))
        self.wait(2)
        
        question1 = Title("Question 2 : Dérivée d'une fonction")
        self.play(
            ReplacementTransform(title1, question1)
        )
        self.wait()
        

        q1_txt = r"Soit \(f\) la fonction définie sur \(]0 ; +\infty[\) par :"
        q1_txt += r"\[f(x) = x^2\ln(x)\]"
        q1 = Tex(q1_txt).scale(0.75)

        q12 = r"L'expression de la fonction dérivée de \(f\) est : "
        q1_q = Tex(q12).next_to(q1, DOWN).scale(0.75)

        a = Tex(r"a. \(f'(x) = 2x\ln(x)\)")
        c = Tex(r"c. \(f'(x) = 2\)")
        b = Tex(r"b. \(f'(x) = x(2\ln(x) + 1)\)")
        d = Tex(r"d. \(f'(x) = x\)")
        
        m1 = MobjectMatrix(
            [[a, c], [b, d]],
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

        solution1 = Title("Réponse b")

        r1m = MathTex(r"f(x) = x^2\ln(x) = uv")
        r2m = MathTex(r"(uv)' = u'v + uv'")
        r3m = MathTex(r"u = x^2\Rightarrow u' = 2x")
        r4m = MathTex(r"v = \ln(x)\Rightarrow v' = \dfrac{1}{x}")
        
        p = [r1m, r2m, r3m, r4m]
        
        self.play(
            ReplacementTransform(attention_rep, solution1),
            ReplacementTransform(mobj1, p[0].next_to(title1, 2 * DOWN))
        )
        self.wait()

        for i in range(1, len(p)):
            self.play(Write(p[i].next_to(p[i-1], DOWN)))
            self.wait(2)
        

        l1m = MathTex(r"u'v = 2x\ln(x)").next_to(solution1, 2 * DOWN)

        l2m = MathTex(r"uv' = x^2\times \dfrac{1}{x} = x").next_to(l1m, DOWN)

        l3m = MathTex(r"u'v + uv' = 2x\ln(x) + x").next_to(l2m, DOWN)

        l4m = MathTex(r"f'(x) = x(2\ln(x) + 1)").next_to(l3m, DOWN)

        l = [l1m, l2m, l3m, l4m]
        
        self.play(
            *[ReplacementTransform(p[i], l[i]) for i in range(len(l))]
        )
        self.wait(5)

        mobj1 = VGroup(l1m, l2m, l3m, l4m)

        final = r"f(x) = x^2\ln(x)\Rightarrow f'(x) = x(2\ln(x) + 1)"
        m_final = MathTex(final)
        box_final = SurroundingRectangle(m_final)
        mobj2 = VGroup(m_final, box_final).next_to(solution1, 2 * DOWN)

        self.play(
            ReplacementTransform(mobj1, mobj2)
        )
        self.wait(4)




class ForeignCenterExo1Question3(Scene):
    def construct(self):
        msg1 = "Bac 2023 centres étrangers groupe 1 sujet 1"
        title1 = Title(f"{msg1}")
        self.add(title1.scale(1))
        self.wait(2)

        t = "Question 3 : Primitive, sens de variation et "
        t += "signe d'une fonction"
        question1 = Title(t)
        self.play(
            ReplacementTransform(title1, question1)
        )
        self.wait()
        

        q01_txt = r"On considère une fonction \(h\) "
        q01_txt += r"définie et continue sur \(\mathbb{R}\)"
        q01 = Tex(q01_txt)
    
        q11_txt = r" dont le tableau de variation est "
        q11_txt += r"ci-dessous : "
        q11 = Tex(q11_txt).next_to(q01, DOWN)

        q_1 = VGroup(q01, q11).scale(0.75)
        
        self.play(
            Write(q_1.next_to(title1, DOWN))
        )
        self.wait()

        t01 = MathTex("x")
        t02 = MathTex(r"-\infty")
        t03 = Text(" ")
        t04 = MathTex(r"1")
        t05 = Text(" ")
        t06 = MathTex(r"+\infty")

        ne_arrow = Arrow(DOWN + LEFT, UP + RIGHT)
        
        t11 = Text(" ")
        t12 = Text(" ")
        t13 = Text(" ")
        t14 = Text(" ")
        t15 = Text(" ")
        t16 = MathTex(r"+\infty")

        t21 = Text(" ")
        t22 = Text(" ")
        t23 = Text(" ")
        t24 = Text(" ")
        t25 = ne_arrow.copy()
        t26 = Text(" ")

        t31 = Tex(r"Variations de \(h\)")
        t32 = Text(" ")
        t33 = Text(" ")
        t34 = MathTex(r"0")
        t35 = Text(" ")
        t36 = Text(" ")

        t41 = Text(" ")
        t42 = Text(" ")
        t43 = ne_arrow.copy()
        t44 = Text(" ")
        t45 = Text(" ")
        t46 = Text(" ")

        t51 = Text(" ")
        t52 = MathTex(r"-\infty")
        t53 = Text(" ")
        t54 = Text(" ")
        t55 = Text(" ")
        t56 = Text(" ")

        
        t1 = MobjectTable(
            [
                [t01, t02, t03, t04, t05, t06],
                [t11, t12, t13, t14, t15, t16],
                [t21, t22, t23, t24, t25, t26],
                [t31, t32, t33, t34, t35, t36],
                [t41, t42, t43, t44, t45, t46],
                [t51, t52, t53, t54, t55, t56],
            ]
        ).next_to(q_1, 1.25 * DOWN).scale(0.5)


        
        self.play(
            t1.animate.shift(2.5 * UP)
        )
        self.wait()
        
        self.play(
            t1.animate.shift(3 * LEFT + 0.5 * UP).scale(0.75)
        )
        self.wait()
        
        q02_txt = r"On note \(H\) la primitive de \(h\) "
        q02 = Tex(q02_txt).scale(0.75)

        q12_txt = r"définie sur \(\mathbb{R}\) qui s'annule "
        q12 = Tex(q12_txt).scale(0.75).next_to(q02, DOWN)
        
        q22 = Tex(
            r"en \(0\). Elle vérifie la propriété : "
        ).scale(0.75).next_to(q12, DOWN)

        q_2 = VGroup(q02, q12, q22).next_to(t1, RIGHT)

        self.play(Write(q_2))
        self.wait()

        self.play(q_2.animate.shift(1 * UP + 0.25 * RIGHT))
        self.wait()
        
        a = Tex(r"a. \(H\) est positive sur \(]-\infty ; 0]\)")
        b = Tex(r"b. \(H\) est croissante sur \(]-\infty ; 1]\)")
        c = Tex(r"c. \(H\) est négative sur \(]-\infty ; 1]\)")
        d = Tex(r"d. \(H\) est croissante sur \(\mathbb{R}\)")
        
        m1 = MobjectMatrix(
            [[a], [b], [c], [d]],
            left_bracket="\{",
            right_bracket="\}"
        ).next_to(q_2, DOWN).scale(0.75)
        
        
        self.play(Write(m1))
        self.wait()

        self.play(m1.animate.shift(0.5 * UP + 0.5 * RIGHT))
        self.wait(4)

        mobj1 = Group(m1, t1, q_2, q_1)

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
        
        solution1 = Title("Réponse a")

        r1m = MathTex(r"H' = h").next_to(title1, 2 * DOWN)
        r2m = Tex(
            r"\(\Rightarrow H\) décroissante sur \(]-\infty ; 1]\)"
        ).next_to(r1m, DOWN)
        r3m = Tex(
            r"Or \(H\) s'annule en \(0\)"
        ).next_to(r2m, DOWN)
        r4m = Tex(
            r"Alors \(H\) est positive sur \(]-\infty ; 0]\)"
        ).next_to(r3m, DOWN)
        
        p = [r1m, r2m, r3m, r4m]
        
        self.play(
            ReplacementTransform(attention_rep, solution1),
            ReplacementTransform(mobj1, p[0]),
        )
        self.wait(2)

        self.play(
            *[Write(p[i]) for i in range(1, len(p))]
        )
        self.wait(2)

        self.play(
            *[r.animate.shift(2 * LEFT) for r in p]
        )
        self.wait(4)

        mobj1 = VGroup(r1m, r2m, r3m, r4m)

        final = Tex(r"\(H\) est positive sur \(]-\infty ; 0]\)")
        box_final = SurroundingRectangle(final)
        mobj2 = VGroup(final, box_final).next_to(solution1, 2 * DOWN)

        self.play(
            ReplacementTransform(mobj1, mobj2)
         )
        self.wait(5)


class ForeignCenterExo1Question4(Scene):
    def construct(self):
        msg1 = "Bac 2023 centres étrangers groupe 1 sujet 1"
        title1 = Title(f"{msg1}")
        self.add(title1.scale(0.75))
        self.wait(2)
        
        question1 = Title("Question 4 : Algorithmique").scale(0.75)
        self.play(
            ReplacementTransform(title1, question1)
        )
        self.wait()
        

        q41_txt = r"Soit deux réels \(a\) et \(b\) avec \(a < b\)."
        q41 = Tex(q41_txt)
        
        q42_txt = r"On considère une fonction \(f\) définie, "
        q42_txt += r"continue, strictement croissante sur "
        q42 = Tex(q42_txt).next_to(q41, DOWN)

        q43_txt = r"l'intervalle \([a ; b]\) et qui s'annule "
        q43_txt += r"en un réel \(\alpha\)."
        q43 = Tex(q43_txt).next_to(q42, DOWN)

        q44_txt = r"Parmi les propositions suivantes, la fonction "
        q44_txt += r"en langage Python qui permet "
        q44 = Tex(q44_txt).next_to(q43, DOWN)

        q45_txt = r"de donner une valeur approchée de \(\alpha\) "
        q45_txt += r"à \(0,001\) est : "
        q45 = Tex(q45_txt).next_to(q44, DOWN)

        q4_list = [q41, q42, q43, q44, q45]
        q4 = VGroup(*q4_list).next_to(title1, DOWN)

        self.play(Write(q4.scale(0.55)))
        self.wait(2)

        self.play(q4.animate.shift(0.85 * UP))
        self.wait(2)
        
        code_a = """a.
def racine(a, b):
    while abs(b - a) >= 0.001: 
        m = (a + b)/2
        if f(m) < 0:
            b = m
        else:
            a = m
    return m
"""        
        a = Code(
            code=code_a,
            tab_width=4,
            background="window",
            language="Python",
            font="Monospace"
        )
        
        code_c = """c.
def racine(a, b): 
    (a + b)/2 
    while abs(b - a) <= 0.001
        if f(m) < 0:
            a = m
        else:
            b = m
    return m
"""        
        c =  Code(
            code=code_c,
            tab_width=4,
            background="window",
            language="Python",
            font="Monospace"
        )
        
        code_b = """b.
def racine(a, b):
    (a + b)/2 
    while abs(b - a) >= 0.001
        if f(m) < 0:
            a = m
        else:
            b = m
    return m
"""
    
        b =  Code(
            code=code_b,
            tab_width=4,
            background="window",
            language="Python",
            font="Monospace"
        )
        
        code_d = """d.
def racine(a, b): 
    while abs(b - a) >= 0.001:
        m = (a + b)/2
        if f(m) < 0:
            a = m
        else:
            b = m
    return m
"""
   
        d =  Code(
            code=code_d,
            tab_width=4,
            background="window",
            language="Python",
            font="Monospace"
        )
        
        m1 = MobjectMatrix(
            [[a, c], [b, d]],
            v_buff=4.25,
            h_buff=10,
            left_bracket="\{",
            right_bracket="\}"
        ).next_to(q4, DOWN).scale(0.55)
        

        self.play(
            m1.animate.shift(1.95 * UP)
        )
        self.wait(4)

        mobj1 = VGroup(m1, q4)

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
        
        solution1 = Title("Réponse d")

        self.play(
            ReplacementTransform(attention_rep, solution1)
        )
        self.wait(2)
        
        s1_txt = r"On veut encadrer \(\alpha\) à \(0,001\) près."
        s1 = Tex(s1_txt).next_to(solution1, DOWN)
        s2_txt = r"Donc on continue tant que l'écart est "
        s2_txt += r"\(\geqslant 0.001\)"
        s2 = Tex(s2_txt).next_to(s1, DOWN)
        s3_txt = r"Puisque la fonction est strictement croissante, si "
        s3 = Tex(s3_txt).next_to(s2, DOWN)
        s4_txt = r"l'image du milieu \(\left(m = \dfrac{a+b}{2}\right)\) "
        s4_txt += r"est négative \(\left(f(m) < 0\right)\) "
        s4 = Tex(s4_txt).next_to(s3, DOWN)
        s5_txt = r"alors l'antécédent de zéro est plus loin "
        s5_txt += r"(\(\alpha\in [m ; b]\))."
        s5 = Tex(s5_txt).next_to(s4, DOWN)
        s6_txt = r"Donc on déplace l'intervalle vers la droite "
        s6_txt += r"(\(a = m\))."
        s6 = Tex(s6_txt).next_to(s5, DOWN)
        s7_txt = r"Sinon c'est l'inverse (\(b = m\))."
        s7 = Tex(s7_txt).next_to(s6, DOWN)

        s4 = VGroup(s1, s2, s3, s4, s5, s6, s7).next_to(solution1, DOWN)
        self.play(
            ReplacementTransform(mobj1, s4)
        )
        self.wait(4)

        d =  Code(
            code=code_d,
            tab_width=4,
            background="window",
            language="Python",
            font="Monospace"
        )
        
        self.play(
            ReplacementTransform(s4, d.next_to(solution1, 2 * DOWN))
            )

        self.wait(5)
        

class ForeignCenterExo1Question5(Scene):
    def construct(self):
        msg1 = "Bac 2023 centres étrangers groupe 1 sujet 1"
        title1 = Title(f"{msg1}")
        self.add(title1.scale(1))
        self.wait(2)
        
        question1 = Title("Question 5 : Probabilités")
        self.play(
            ReplacementTransform(title1, question1)
        )
        self.wait()
        

        q1_txt = r"Une urne contient 10 boules indiscernables au toucher "
        q1_txt += r"dont 7 sont bleues "
        q1 = Tex(q1_txt).scale(0.75)

        q12_txt = r"et les autres vertes. On effectue trois tirages "
        q12_txt += r"successifs avec remise. "
        q12 = Tex(q12_txt).next_to(q1, DOWN).scale(0.75)

        q13_txt = r"La probabilité d'obtenir exactement "
        q13_txt += r"deux boules vertes est : "
        q13 = Tex(q13_txt).next_to(q12, DOWN).scale(0.75)

        a_txt = r"a. \left(\dfrac{7}{10}\right)^2\times "
        a_txt += r"\dfrac{3}{10}"
        a = MathTex(a_txt)
        
        c_txt = r"c. \binom{10}{2}\left(\dfrac{7}{10}\right) "
        c_txt += r"\left(\dfrac{3}{10}\right)^2"
        c = MathTex(c_txt)

        b_txt = r"b. \left(\dfrac{3}{10}\right)^2"
        b = MathTex(b_txt)

        d_txt = r"d. \binom{3}{2}\left(\dfrac{7}{10}\right) "
        d_txt += r"\left(\dfrac{3}{10}\right)^2"
        d = MathTex(d_txt)
        
        m1 = MobjectMatrix(
            [[a, c], [b, d]],
            v_buff=2.5,
            h_buff=10,
            left_bracket="\{",
            right_bracket="\}"
        ).next_to(q13, DOWN).scale(0.75)
        
        mobj1 = VGroup(q1, q12, q13, m1)


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
        solution1 = Title("Réponse d")

        r1m = Tex(r"Soit \(X\) la variable aléatoire comptant ")
        r2m = Tex(r"le nombre de boules vertes obtenues avec ")
        r3m = Tex(r"3 tirages. Cette variable suit une loi binomiale ")
        r4m = Tex(r"de paramètres \(n = 3\) et \(p = \dfrac{3}{10}\).")
        r5m = Tex(r"D'où le résultat.")
        r6_txt = r"P(X = 2) = \binom{3}{2}\left(\dfrac{3}{10}\right)^2"
        r6_txt += r"\left(\dfrac{7}{10}\right)"
        r6m = MathTex(r6_txt)
        
        r = VGroup(
            r1m,
            r2m.next_to(r1m, DOWN),
            r3m.next_to(r2m, DOWN),
            r4m.next_to(r3m, DOWN),
            r5m.next_to(r4m, DOWN),
            r6m.next_to(r5m, DOWN),
        )
        
        self.play(
            ReplacementTransform(attention_rep, solution1),
        )
        self.wait(2)

        self.play(
            ReplacementTransform(mobj1, r.next_to(solution1, DOWN))
        )
        self.wait(4)

        final = r"P(X = 2) = \binom{3}{2}\left(\dfrac{3}{10}\right)^2"
        final += r"\left(\dfrac{7}{10}\right)"
        m_final = MathTex(final)
        box_final = SurroundingRectangle(m_final)
        mobj2 = VGroup(m_final, box_final).next_to(solution1, 2 * DOWN)

        self.play(
            ReplacementTransform(r, mobj2)
        )
        self.wait(4)
        

##################################################
# Centres étrangers Groupe 1 Sujet 1
##################################################

# Exo 4 Affirmation 1
class ForeignCenterExo4Affirmation1(Scene):
    def construct(self):
        msg1 = "Bac 2023 centres étrangers groupe 1 sujet 1 exo 4"
        title1 = Title(f"{msg1}")
        self.add(title1.scale(1))
        self.wait(2)
        
        affirmation1 = Title("Affirmation 1")
        self.play(
            ReplacementTransform(title1, affirmation1)
        )
        self.wait()
        

        txt_part1 = r"Un biologiste a modélisé l'évolution d'une "
        txt_part1 += r"population de bactéries "
        part1 = Tex(txt_part1).next_to(affirmation1, DOWN).scale(0.95)
        
        txt_part2 = r"(en milliers d'entités) par la \(f\) fonction "
        txt_part2 += r"définie sur \([0; +\infty [\)"
        part2 = Tex(txt_part2).next_to(part1, DOWN)

        txt_part3 = r"\[f(t) = e^3 - e^{-0,5t^2 + t + 2}\]"
        part3 = Tex(txt_part3).next_to(part2, DOWN)


        aff1 = Tex(
            "Affirmation 1 : La population augmente en permanence."
        ).next_to(part3, 2 * DOWN)
        mobj1 = VGroup(part1, part2, part3, aff1)


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
        
        solution1 = Title("Affirmation fausse")

        r10 = r"(e^3)' = 0"
        r11 = r"(e^u)' = u'e^u"
        r12 = r"u = -0,5t^2 + t + 2\Rightarrow u' = 2(-0,5)t + 1 = 1 - t"
        r13 = r"f'(t) = (1 - t)(-e^{-0,5t^2 + t + 2})"
        r14 = r"f'(t) = (t - 1)e^{-0,5t^2 + t + 2}"
        
        rep = [r10, r11, r12, r13, r14]
        p = [MathTex(r) for r in rep]
        
        self.play(
            ReplacementTransform(attention_rep, solution1),
            ReplacementTransform(
                mobj1,
                p[0].next_to(affirmation1, 2 * DOWN)
            )
        )
        self.wait()

        for i in range(1, len(p)):
            self.play(Write(p[i].next_to(p[i-1], DOWN)))
            self.wait(2)
        

        l1 = r"e^{-0,5t^2 + t + 2} > 0"
        l1m = MathTex(l1).next_to(solution1, 2 * DOWN)

        l2 = r"t - 1 < 0 \iff t < 1"
        l2 += r"\Rightarrow f' < 0 "
        l2m = MathTex(l2).next_to(l1m, DOWN)

        l = [l1m, l2m]
        
        self.play(
            *[ReplacementTransform(p[i], l[i]) for i in range(len(l))],
            *[FadeOut(p[i]) for i in range(2, len(p))]
        )
        self.wait(3)

        mobj1 = VGroup(l1m, l2m)

        final = r"La population diminue durant la première heure."
        m_final = Tex(final)
        box_final = SurroundingRectangle(m_final)

        mobj2 = VGroup(m_final, box_final)

        self.play(
            ReplacementTransform(
                mobj1,
                mobj2.next_to(solution1, 2 * DOWN)
            )
        )
        self.wait(4)


# Exo 4 Affirmation 2
class ForeignCenterExo4Affirmation2(Scene):
    def construct(self):
        msg1 = "Bac 2023 centres étrangers groupe 1 sujet 1 exo 4"
        title1 = Title(f"{msg1}")
        self.add(title1.scale(1))
        self.wait(2)
        
        affirmation2 = Title("Affirmation 2")
        self.play(
            ReplacementTransform(title1, affirmation2)
        )
        self.wait()
        

        txt_part1 = r"Un biologiste a modélisé l'évolution d'une "
        txt_part1 += r"population de bactéries "
        part1 = Tex(txt_part1).next_to(affirmation2, DOWN).scale(0.95)
        
        txt_part2 = r"(en milliers d'entités) par la \(f\) fonction "
        txt_part2 += r"définie sur \([0; +\infty [\)"
        part2 = Tex(txt_part2).next_to(part1, DOWN)

        txt_part3 = r"\[f(t) = e^3 - e^{-0,5t^2 + t + 2}\]"
        part3 = Tex(txt_part3).next_to(part2, DOWN)


        aff1 = Tex("Affirmation 2 : ").next_to(part3, 2 * DOWN)
        aff1_2 = Tex(
            "À très long terme, la population dépassera 21 000 bactéries."
        ).next_to(aff1, DOWN)
        mobj1 = VGroup(part1, part2, part3, aff1, aff1_2)


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
        
        solution1 = Title("Affirmation fausse.")

        r10 = r"f(t) = e^3 - e^{-0,5t^2 + t + 2}"
        r11 = r"f'(t) = (t - 1)e^{-0,5t^2 + t + 2}"
        r12 = r"e^{-0,5t^2 + t + 2} > 0"
        r13 = r"t > 1 \iff f' > 0"
        r14 = r"\lim_{t\to + \infty} -0,5t^2 + t + 2 = -\infty"
        r15 = r"-0,5t^2 + t + 2 = t^2\left(-0,5 + \dfrac{t}{t^2} + "
        r15 += r"\dfrac{2}{t^2}\right)"
        r16 = r"\lim_{t\to + \infty}\dfrac{t}{t^2} = 0 = "
        r16 += r"\lim_{t\to + \infty}\dfrac{2}{t^2}"
        r17 = r"\lim_{t\to + \infty}e^{-0,5t^2 + t + 2} = 0"
        r18 = r"\lim_{t\to + \infty}f(t) = e^3 \simeq 20,086 < 21"
        
        rep = [r10, r11, r12, r13, r14, r15, r16, r17, r18]
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

        #m_part1 = VGroup(*p[:len(p) // 2])
        
        self.play(
            *[
                ReplacementTransform(
                    p[i],
                    p[len(p) // 2 + i].next_to(p[i], 2 * DOWN)
                ) for i in range(len(p) // 2)
            ]
        )
        self.wait(5)

        self.play(
            Write(p[-1].next_to(affirmation2, 2 * DOWN))
        )
        self.wait(2)

        box_res = SurroundingRectangle(p[-1])
        self.play(
            Write(box_res)
        )
        self.wait(2)

        mobj1 = VGroup(box_res, *p)

        final = r"La population ne dépassera pas 21 000 bactéries."
        m_final = Tex(final)
        box_final = SurroundingRectangle(m_final)

        mobj2 = VGroup(m_final, box_final)

        self.play(
            ReplacementTransform(
                mobj1,
                mobj2.next_to(solution1, 2 * DOWN)
            )
        )
        self.wait(4)

        

# Exo 4 Affirmation 3
class ForeignCenterExo4Affirmation3(Scene):
    def construct(self):
        msg1 = "Bac 2023 centres étrangers groupe 1 sujet 1 exo 4"
        title1 = Title(f"{msg1}")
        self.add(title1.scale(1))
        self.wait(2)
        
        affirmation3 = Title("Affirmation 3")
        self.play(
            ReplacementTransform(title1, affirmation3)
        )
        self.wait()
        

        txt_part1 = r"Un biologiste a modélisé l'évolution d'une "
        txt_part1 += r"population de bactéries "
        part1 = Tex(txt_part1).next_to(affirmation3, DOWN).scale(0.95)
        
        txt_part2 = r"(en milliers d'entités) par la \(f\) fonction "
        txt_part2 += r"définie sur \([0; +\infty [\)"
        part2 = Tex(txt_part2).next_to(part1, DOWN)

        txt_part3 = r"\[f(t) = e^3 - e^{-0,5t^2 + t + 2}\]"
        part3 = Tex(txt_part3).next_to(part2, DOWN)


        aff3 = Tex("Affirmation 3 : ").next_to(part3, 2 * DOWN)
        aff3_2 = Tex(
            "La population de bactéries aura un effectif de 10 000 "
        ).next_to(aff3, DOWN)
        aff3_3 = Tex(
            "à deux reprises."
        ).next_to(aff3_2, DOWN)
        mobj1 = VGroup(part1, part2, part3, aff3, aff3_2, aff3_3)


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
        
        solution1 = Title("Affirmation vraie.")

        r10 = r"f(t) = e^3 - e^{-0,5t^2 + t + 2}"
        r11 = r"f(0) = e^3 - e^2 \simeq 12,696 > 10"
        r12 = r"t\in [0; 1[\iff f' < 0"
        r13 = r"(TVI) \Rightarrow f(t)\in ]f(1) ; f(0)]"
        r14 = r"f(1) = e^3 - e^{2,5}\simeq 7,903 < 10"
        r15 = r"t\in ]1 ; +\infty \iff f' > 0"
        r15 += r"(TVI) \Rightarrow f(t)\in ]f(1) ; e^3]"
        r16 = r"\lim_{t\to + \infty}f(t) = e^3 \simeq 20,086 > 10"
        
        rep = [r10, r11, r12, r13, r14, r15, r16]
        p = [MathTex(r) for r in rep]
        
        self.play(
            ReplacementTransform(attention_rep, solution1),
            ReplacementTransform(
                mobj1,
                p[0].next_to(affirmation3, 2 * DOWN)
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
                    p[len(p) // 2 + i].next_to(p[i], 2 * DOWN)
                ) for i in range(len(p) // 2)
            ]
        )
        self.wait(5)

        self.play(
            Write(p[-1].next_to(affirmation3, 2 * DOWN))
        )
        self.wait(2)

        box_res = SurroundingRectangle(p[-1])
        self.play(
            Write(box_res)
        )
        self.wait(2)

        mobj1 = VGroup(box_res, *p)

        final = r"La population atteindra 10 000 bactéries 2 fois."
        m_final = Tex(final)
        box_final = SurroundingRectangle(m_final)

        mobj2 = VGroup(m_final, box_final)

        self.play(
            ReplacementTransform(
                mobj1,
                mobj2.next_to(solution1, 2 * DOWN)
            )
        )

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
# Réunion 28 mars 2023 
##################################################

# Exo 3 Partie Question 1
class ReunionExo3PartAQuestion1(Scene):
    def construct(self):
        msg1 = "Bac Réunion 28 mars 2023 Exercice 3 Partie A"
        title1 = Title(f"{msg1}")
        self.add(title1.scale(1))
        self.wait(2)

        intro = [
            r"On considère la suite \((u_n)\) définie par \(u_0 = 3\) et, pour tout entier naturel \(n\),",
            r"\(u_{n+1} = \dfrac{1}{2}u_n + \dfrac{1}{2}n + 1\)."
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
        q1 = Tex(r"1. La valeur de \(u_2\) est égale à : ")
        a = r"a. \(\dfrac{11}{4}\)"
        b = r"b. \(\dfrac{13}{2}\)"
        c = r"c. 3,5"
        d = r"d. 2,7"
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
        
        a00 = r"\(u_0 = 3\)"
        a01 = r"\(u_{0 + 1} = \dfrac{1}{2}\times 3 + \dfrac{1}{2}\times 0 + 1\)"
        a02 = r"\(u_1 = \dfrac{3}{2} + \dfrac{2}{2}\)"
        a03 = r"\(u_1 = \frac{5}{2}\)"
        a04 = r"\(u_{1 + 1} = \dfrac{1}{2}\times \dfrac{5}{2} + \dfrac{1}{2}\times 1 + 1\)"
        a05 = r"\(u_2 = \dfrac{5}{4} + \dfrac{1}{2} + \dfrac{2}{2}\)"
        a06 = r"\(u_2 = \dfrac{5}{4} + \dfrac{3}{2}\)"
        a07 = r"\(u_2 = \dfrac{5}{4} + \dfrac{6}{4}\)"
        a08 = r"\(u_2 = \dfrac{11}{4}\)"
        
        a_r = [a00, a01, a02, a03, a04, a05, a06, a07, a08]
        a_proof = [Tex(d).scale(0.75) for d in a_r]

        

        disp_calculations(self, 
            previous_mobj=mobj1,
            calcs=a_proof,
            next2obj=intro_tex[-1],
            direction=DOWN
        )

        box_sol = SurroundingRectangle(a_proof[-1], color=GREEN)
        self.play(Write(box_sol))
        self.wait()
        
        


# Question 2
class ReunionExo3PartAQuestion2(Scene):
    def construct(self):
        msg1 = "Bac Réunion 28 mars 2023 Exercice 3 Partie A"
        title1 = Title(f"{msg1}")
        self.add(title1.scale(1))
        self.wait(2)

        intro = [
            r"On considère la suite \((u_n)\) définie par \(u_0 = 3\) et, pour tout entier naturel \(n\),",
            r"\(u_{n+1} = \dfrac{1}{2}u_n + \dfrac{1}{2}n + 1\)."
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
        q2 = Tex(r"2. La suite \((v_n)\) définie, pour tout entier naturel \(n\), par \(v_n = u_n - n\) est : ")
        a = r"a. arithmétique de raison \(\dfrac{1}{2}\)"
        b = r"b. géométrique de raison \(\dfrac{1}{2}\)"
        c = r"c. constante"
        d = r"d. ni arithmétique, ni géométrique"
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
        sol_b = ent[1]
        box_b = SurroundingRectangle(sol_b)
        solution2 = Title("Réponse b")
        self.play(
            ReplacementTransform(attention_rep, solution2),
            Write(box_b)
        )
        self.wait()

        
        explanation = Title("Explications")

        
        self.play(
            ReplacementTransform(solution2, explanation)
        )
        self.wait(2)

        
        b00 = r"\(v_{n + 1} = u_{n + 1} - (n + 1)\)"
        b01 = r"\(v_{n + 1} = \dfrac{1}{2}u_n + \dfrac{1}{2}n + 1 - n - 1\)"
        b02 = r"\(v_{n + 1} = \dfrac{1}{2}u_n - \dfrac{1}{2}n\)"
        b03 = r"\(v_{n + 1} = \dfrac{1}{2}(u_n - n)\)"
        b04 = r"\(v_{n + 1} = \dfrac{1}{2}v_n\)"
        
        b_r = [b00, b01, b02, b03, b04]
        b_proof = [Tex(d).scale(0.75) for d in b_r]

        disp_calculations(self, 
            previous_mobj=None,
            calcs=b_proof,
            next2obj=mobj1,
            direction=DOWN
        )

        box_sol = SurroundingRectangle(b_proof[-1], color=GREEN)
        self.play(Write(box_sol))
        self.wait()


# Question 3
class ReunionExo3PartAQuestion3(Scene):
    def construct(self):
        msg1 = "Bac Réunion 28 mars 2023 Exercice 3 Partie A"
        title1 = Title(f"{msg1}")
        self.add(title1.scale(0.85))
        self.wait(2)

        intro = [
            r"On considère la suite \((u_n)\) définie par \(u_0 = 3\) et, pour tout entier naturel \(n\),",
            r"\(u_{n+1} = \dfrac{1}{2}u_n + \dfrac{1}{2}n + 1\)."
        ]

        intro_tex = [Tex(i) for i in intro]
        self.play(
            Write(intro_tex[0].scale(0.65).next_to(title1, DOWN))
        )
        self.wait()
        for i in range(len(intro) - 1):
            self.play(
                Write(intro_tex[i+1].scale(0.65).next_to(intro_tex[i], DOWN))
            )
            self.wait()

        question3 = Title("Question 3").scale(0.75)
        
        justified_text = """n désigne un entier naturel non nul.\n
On rappelle qu'en langage Python\n
"\(i\quad in\quad range(n)\)"\n
signifie que i varie de 0 à n - 1."""

        code_b = """
def terme(n):
    U = 3
    for i in range(n):
        ...
    return U
"""        
        b = Code(
            code=code_b,
            tab_width=4,
            background="window",
            language="Python",
            font="Monospace"
        ).scale(0.65)
        reminder = Tex(justified_text).scale(0.65)
        t = VGroup(reminder, b.next_to(reminder, 1.25 * RIGHT))
        q3 = [
            Tex(r"3. On considère la fonction ci-dessous, écrite de manière incomplète en langage Python.").scale(0.65),
            t,
            Tex(r"Pour que terme(n) renvoie la valeur de \(u_n\), on peut compléter la ligne 4 par : ").scale(0.65)
        ]


        disp_tex_list(self, 
            previous_mobj=None,
            tex_list=q3,
            next2obj=intro_tex[-1],
            direction=DOWN
        )
        
        a = r"a. U = U/2 + (i + 1)/2 + 1"
        b = r"b. U = U/2 + n/2 + 1"
        c = r"c. U = U/2 + (i - 1)/2 + 1"
        d = r"d. U = U/2 + i/2 + 1"
        
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
            ReplacementTransform(question3, noter.scale(0.65))
        )
        self.wait(4)

        attention_rep = Title("Cherchez avant de regarder le corrigé")
        self.play(
            ReplacementTransform(noter, attention_rep.scale(0.65))
        )
        self.wait(4)

        ent = m1.get_entries()
        sol_c = ent[2]
        box_c = SurroundingRectangle(sol_c)
        solution3 = Title("Réponse c")
        self.play(
            ReplacementTransform(attention_rep, solution3),
            Write(box_c)
        )
        self.wait()

        
        explanation = Title("Explications")
        
        self.play(
            ReplacementTransform(solution3, explanation.scale(0.65)),
            Unwrite(box_c)
        )
        self.wait(2)

        exp00 = r"Par définition \(u_n = u_{n - 1} + 1\)"
        exp01 = r"Donc \(u_n = \dfrac{1}{2}u_{n - 1} + \dfrac{n - 1}{2} + 1\)"
        exp02 = r"D'après le rappel, range(n) va jusqu'à n - 1"
        exp03 = r"Donc le dernier terme calculé est bien \(u_n\)"
        exp04 = r"et à chaque étape on calcule \(u_i\) en fonction de \(i - 1\)"
        exp05 = r"D'où la réponse U=U/2 + (i-1)/2 + 1"

        exps = [exp00, exp01, exp02, exp03, exp04, exp05]
        exp_tex = [Tex(e).scale(0.65) for e in exps]
        disp_calculations(self, 
            previous_mobj=m1,
            calcs=exp_tex,
            next2obj=q3[-1],
            direction=DOWN
        )
        
        


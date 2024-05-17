from manim import *
import manim
from math import e, pi
import math
from PIL import Image

def disp_sub(self, lang):
    if lang.lower() == "en":
        written, phon = "Subscribe", "/səbˈskraɪb/"
        sub_pic = SVGMobject("/Users/digitalnomad/Documents/pics/svg/subscribe.svg")
        sub_scale = 0.8 
    elif lang.lower() == "fr":
        written, phon = "Abonnez-vous", "/abɔne vu/"
        sub_pic = ImageMobject("/Users/digitalnomad/Documents/pics/png/sabonner.png")
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
# Bac 2024 Sujet 0
##################################################

# Exo 5 Question 1
class Bac2024Sujet0Exo5Question1(Scene):
    def construct(self):
        msg1 = "Bac 2024 Sujet 0 Exercice 5"
        title1 = Title(f"{msg1}")
        self.add(title1.scale(1))
        self.wait(2)

        
        question1 = Title("Question 1")
        q1_txt = [
            r"1. Sur l'intervalle \([0; 2\pi]\), l'équation "
            r"\(\sin(x) = 0,1\) admet :",
        ]
        q1 = [Tex(t).scale(0.75) for t in q1_txt]
        
        disp_tex_list(self, 
            previous_mobj=None,
            tex_list=q1,
            next2obj=title1,
            direction=DOWN
        )
        a = r"a. zéro solution"
        b = r"b. une solution"
        c = r"c. deux solutions"
        d = r"d. quatre solutions"
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
        sol_c = ent[2]
        box_c = SurroundingRectangle(sol_c)
        solution1 = Title("Réponse c")
        self.play(
            ReplacementTransform(attention_rep, solution1),
            Write(box_c)
        )
        self.wait()

        
        explanation = Title("Explications")

        self.play(
            Unwrite(box_c),
            ReplacementTransform(solution1, explanation.scale(0.75))
        )
        self.wait()
        
        C00 = r"La fonction \(f(x) = \sin(x)\) est dérivable, "
        C00 += r"et donc continue, sur \([0 ; 2\pi]\)."
        C01 = r"Sa dérivée est la fonction \(f'(x) = \sin'(x) = \cos(x)\). "
        C01 += r"Et \(\sin(x) \leqslant 0\) sur \([\pi ; 2\pi]\). "
        C02 = r"\(\cos(x) > 0\) (donc \(\sin\) est strictement croissante) "
        C02 += r"sur l'intervalle \(I_1 = \left]0 ; \frac{\pi}{2}\right[ \), "
        C03 = r"or \(\sin(0) = 0 < 0,1 < 1 = \sin\left(\frac{\pi}{2} \right)\)."
        C03 += r" D'après le théorème de la bijection (TVI + "
        C04 = r"monotonie stricte) il existe un unique \(\alpha\in I_1\) "
        C04 += r"tel que \(\sin(\alpha) = 0,1\)."
        C05 = r"\(\cos(x) < 0\) (donc \(\sin\) est strictement décroissante) "
        C05 += r"sur l'intervalle \(I_2 = \left]\frac{\pi}{2} ; \pi\right[ \), "
        C06 = r"or \(\sin(\pi) = 0 < 0,1\). "
        C06 += r"D'après le théorème de la bijection "
        C07 = r"il existe un unique \(\beta\in I_2\) "
        C07 += r"tel que \(\sin(\beta) = 0,1\)."
        
        C = [C00, C01, C02, C03, C04, C05, C06, C07]
        dC = [Tex(d).scale(0.75) for d in C]
        dCVGroup = VGroup(*dC)
        

        disp_tex_list(self, 
            previous_mobj=m1,
            tex_list=dC,
            next2obj=q1[-1],
            direction=DOWN
        )

        x_vals = [r"0", r"\dfrac{\pi}{2}", r"\pi"]
        cos_vals = [r"1", r"0", "-1"]
        sin_vals = [r"0", r"1", r"0"]
        t0 = MathTable(
            [x_vals, cos_vals, sin_vals],
            row_labels=[
                MathTex(r"x"),
                MathTex(r"f'(x) = \cos(x)"),
                MathTex(r"f(x) = \sin(x)")
            ],
            h_buff=1
        ).scale(0.85)
        self.play(
            ReplacementTransform(dCVGroup, t0.next_to(q1[-1], DOWN))
        )
        self.wait(2)

        axes = Axes(
            x_range=[0, 5, 0.5],
            y_range=[-1.25, 1.25, 0.25],
            x_length=10,
            tips=False,
        )
        #axes_labels = axes.get_axis_labels()
        
        sin_graph = axes.plot(lambda x: np.sin(x), color=BLUE)
        sin_label = axes.get_graph_label(
            sin_graph, r"\sin(x)", x_val=PI, direction=UP
        )

        horiz_line0 = axes.plot(lambda x: 0, color=RED)
        horiz_line0_label = axes.get_graph_label(
            horiz_line0, r"y = 0", x_val=0, direction=DOWN/2
        )
        
        horiz_line01 = axes.plot(lambda x: 0.1, color=GREEN)
        horiz_line01_label = axes.get_graph_label(
            horiz_line01, r"y = 0,1", x_val=PI/2, direction=UP
        )

        horiz_line1 = axes.plot(lambda x: 1, color=RED)
        horiz_line1_label = axes.get_graph_label(
            horiz_line1, r"y = 1", x_val=1.5*PI, direction=UP/4
        )
        vert_line_pi2 = axes.get_vertical_line(
            axes.i2gp(PI/2, sin_graph), color=YELLOW, line_func=Line
        )
        vert_line_pi2_label = axes.get_graph_label(
            sin_graph, "x = \dfrac{\pi}{2}", x_val=PI/2,
            direction=UP/10, color=YELLOW
        ).scale(0.75)

        vert_line_3pi2 = axes.get_vertical_line(
            axes.i2gp(3*PI/2, sin_graph), color=YELLOW, line_func=Line
        )
        vert_line_3pi2_label = axes.get_graph_label(
            sin_graph, "x = \dfrac{3\pi}{2}", x_val=3*PI/2,
            direction=UL, color=YELLOW
        ).scale(0.75)

        plot = VGroup(
            axes,
            sin_graph,
            horiz_line0,
            horiz_line01,
            horiz_line1,
            vert_line_pi2,
            vert_line_3pi2
        ).scale(0.75)
        
        labels = VGroup(
            #axes_labels,
            sin_label,
            horiz_line0_label,
            horiz_line01_label,
            horiz_line1_label,
            vert_line_pi2_label,
            vert_line_3pi2_label
        )
        
        plot_and_labels = VGroup(plot, labels)
        
        self.play(
            ReplacementTransform(t0, plot_and_labels.next_to(q1[-1], DOWN)),
        )
        self.wait()


class Subscribe(Scene):
    def construct(self):
        msg1 = "Abonnez-vous"
        title1 = Title(f"{msg1}")
        self.add(title1.scale(1))
        self.wait(2)

        credits_txt = [
            r"Animations réalisées par Laurent Garnier",
            r"Vous pouvez me contactez par mail "
            r"prenom.nom.superprofATgmail.com",
            r"si vous souhaitez travailler avec moi.",
            r"Merci pour votre attention."
        ]
        dCredits = [Tex(d).scale(0.75) for d in credits_txt]
        dCVGroup = VGroup(*dCredits)
        

        disp_tex_list(self, 
            previous_mobj=None,
            tex_list=dCredits,
            next2obj=title1,
            direction=DOWN
        )

        self.wait(2)

        disp_sub(self, lang="FR")
        
# Moving Camera 
class Exo5Question1MovingCamera(MovingCameraScene):
    def construct(self):
        self.camera.frame.save_state()

        # create the axes and the curve
        ax = Axes(x_range=[-1, 7], y_range=[-2, 2])
        
        sin_graph = ax.plot(
            lambda x: np.sin(x),
            color=BLUE,
            x_range=[0, 2 * PI]
        )
        sin_label = ax.get_graph_label(
            sin_graph, r"y = \sin(x)", x_val=PI/2, direction=UP
        )

        level_line = ax.plot(lambda x: 0.1, color=GREEN, x_range=[0, 2 * PI])
        level_label = ax.get_graph_label(
            level_line, r"y = 0,1", x_val=1.5*PI, direction=UP
        )
        
        # create dots based on the sin_graph
        moving_dot = Dot(ax.i2gp(sin_graph.t_min, sin_graph), color=ORANGE)
        dot_1 = Dot(ax.i2gp(sin_graph.t_min, sin_graph))
        dot_2 = Dot(ax.i2gp(sin_graph.t_max, sin_graph))

        self.add(
            ax,
            sin_graph, sin_label,
            dot_1, dot_2, moving_dot,
            level_line, level_label
        )
        self.play(self.camera.frame.animate.scale(0.5).move_to(moving_dot))

        def update_curve(mob):
            mob.move_to(moving_dot.get_center())

        self.camera.frame.add_updater(update_curve)
        self.play(
            MoveAlongPath(moving_dot, sin_graph, rate_func=there_and_back),
            run_time=8
        )
        self.wait(2)

        vert_line_pi36 = ax.get_vertical_line(
            ax.i2gp(PI/36, sin_graph), color=YELLOW, line_func=Line
        )
        vert_line_pi36_label = ax.get_graph_label(
            sin_graph, "x = \dfrac{\pi}{36}", x_val=PI/36,
            direction=DOWN/2, color=YELLOW
        ).scale(0.5)
        
        vert_line_pi18 = ax.get_vertical_line(
            ax.i2gp(PI/18, sin_graph), color=YELLOW, line_func=Line
        )
        vert_line_pi18_label = ax.get_graph_label(
            sin_graph, "x = \dfrac{\pi}{18}", x_val=PI/18,
            direction=UP/2, color=YELLOW
        ).scale(0.5)
        
        pi6 = VGroup(
            vert_line_pi36, vert_line_pi36_label,
            vert_line_pi18, vert_line_pi18_label
        )
        self.play(Write(pi6))
        self.wait(2)
                  
        self.camera.frame.remove_updater(update_curve)
        self.play(Restore(self.camera.frame))

        vert_line_35pi36 = ax.get_vertical_line(
            ax.i2gp(35*PI/36, sin_graph), color=YELLOW, line_func=Line
        )
        vert_line_35pi36_label = ax.get_graph_label(
            sin_graph, "x = \dfrac{35\pi}{36}", x_val=35*PI/36,
            direction=UP/2, color=YELLOW
        ).scale(0.5)

        vert_line_17pi18 = ax.get_vertical_line(
            ax.i2gp(17*PI/18, sin_graph), color=YELLOW, line_func=Line
        )
        vert_line_17pi18_label = ax.get_graph_label(
            sin_graph, "x = \dfrac{17\pi}{18}", x_val=17*PI/18,
            direction=DOWN/2, color=YELLOW
        ).scale(0.5)
        
        five_pi6 = VGroup(
            vert_line_35pi36, vert_line_35pi36_label,
            vert_line_17pi18, vert_line_17pi18_label
        )
        self.play(Write(five_pi6))
        self.wait(2)
        
        self.camera.frame.add_updater(update_curve)
        self.play(
            MoveAlongPath(moving_dot, sin_graph, rate_func=there_and_back),
            run_time=8
        )
        self.wait(2)
        
        self.camera.frame.remove_updater(update_curve)
        self.play(Restore(self.camera.frame))
        


class MovingZoomedSceneAround(ZoomedScene):
# contributed by TheoremofBeethoven, www.youtube.com/c/TheoremofBeethoven
    def __init__(self, **kwargs):
        ZoomedScene.__init__(
            self,
            zoom_factor=0.3,
            zoomed_display_height=1,
            zoomed_display_width=6,
            image_frame_stroke_width=20,
            zoomed_camera_config={
                "default_frame_stroke_width": 3,
                },
            **kwargs
        )

    def construct(self):
        dot = Dot().shift(UL * 2)
        image = ImageMobject(np.uint8([[0, 100, 30, 200],
                                       [255, 0, 5, 33]]))
        image.height = 7
        frame_text = Text("Frame", color=PURPLE, font_size=67)
        zoomed_camera_text = Text("Zoomed camera", color=RED, font_size=67)

        self.add(image, dot)
        zoomed_camera = self.zoomed_camera
        zoomed_display = self.zoomed_display
        frame = zoomed_camera.frame
        zoomed_display_frame = zoomed_display.display_frame

        frame.move_to(dot)
        frame.set_color(PURPLE)
        zoomed_display_frame.set_color(RED)
        zoomed_display.shift(DOWN)

        zd_rect = BackgroundRectangle(zoomed_display, fill_opacity=0, buff=MED_SMALL_BUFF)
        self.add_foreground_mobject(zd_rect)

        unfold_camera = UpdateFromFunc(zd_rect, lambda rect: rect.replace(zoomed_display))

        frame_text.next_to(frame, DOWN)

        self.play(Create(frame), FadeIn(frame_text, shift=UP))
        self.activate_zooming()

        self.play(self.get_zoomed_display_pop_out_animation(), unfold_camera)
        zoomed_camera_text.next_to(zoomed_display_frame, DOWN)
        self.play(FadeIn(zoomed_camera_text, shift=UP))
        # Scale in        x   y  z
        scale_factor = [0.5, 1.5, 0]
        self.play(
            frame.animate.scale(scale_factor),
            zoomed_display.animate.scale(scale_factor),
            FadeOut(zoomed_camera_text),
            FadeOut(frame_text)
        )
        self.wait()
        self.play(ScaleInPlace(zoomed_display, 2))
        self.wait()
        self.play(frame.animate.shift(2.5 * DOWN))
        self.wait()
        self.play(self.get_zoomed_display_pop_out_animation(), unfold_camera, rate_func=lambda t: smooth(1 - t))
        self.play(Uncreate(zoomed_display_frame), FadeOut(frame))
        self.wait()

        
# Question 2
class Bac2024Sujet0Exo5Question2(Scene):
    def construct(self):
        msg1 = "Bac 2024 Sujet 0 Exercice 5"
        title2 = Title(f"{msg1}")
        self.add(title2.scale(1))
        self.wait(2)

        question2 = Title("Question 2")
        q2_txt = [
            r"2. On considère la fonction \(f\) définie sur l'intervalle "
            r"\([0 ; \pi]\) par :",
            r"\(f(x) = x + \sin(x)\).",
            r"On admet que \(f\) est deux fois dérivables."
        ]
        q2 = [Tex(t).scale(0.75) for t in q2_txt]
        
        disp_tex_list(self, 
            previous_mobj=None,
            tex_list=q2,
            next2obj=title2,
            direction=DOWN
        )
        a = r"a. La fonction \(f\) est convexe sur l'intervalle \([0 ; \pi]\)"
        b = r"b. La fonction \(f\) est concave sur l'intervalle \([0 ; \pi]\) "
        c = r"c. La fonction \(f\) admet sur l'intervalle \([0 ; \pi]\)"
        c += r"un unique point d'inflexion"
        d = r"d. La fonction \(f\) admet sur l'intervalle \([0 ; \pi]\) "
        d += r"exactement deux points d'inflexion"
        m1 = MobjectMatrix(
            [[Tex(a)], [Tex(b)], [Tex(c)], [Tex(d)]],
            v_buff=0.75,
            h_buff=8,
            left_bracket="\{",
            right_bracket="\}"
        ).scale(0.75)

        
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
            Unwrite(box_b),
            ReplacementTransform(solution2, explanation.scale(0.75))
        )
        self.wait()
        
        B00 = r"La fonction \(f(x) = x + \sin(x)\) est deux fois dérivable, "
        B00 += r"\(f'(x) = 1 + \cos(x)\Rightarrow f''(x) = -\sin(x)\)."
        B01 = r"Or \(\sin(x)\in [0 ; 1]\) pour tout \(x\in [0 ; \pi]\)."
        B02 = r"Donc \(f''(x)\leqslant 0\) ce qui implique que "
        B02 += r"\(f\) soit concave."
        
        B = [B00, B01, B02]
        dB = [Tex(d).scale(0.75) for d in B]
        dBVGroup = VGroup(*dB)
        

        disp_tex_list(self, 
            previous_mobj=m1,
            tex_list=dB,
            next2obj=q2[-1],
            direction=DOWN
        )



# Moving Camera 
class Exo5Question2MovingCamera(MovingCameraScene):
    def construct(self):
        self.camera.frame.save_state()

        # create the axes and the curve
        ax = Axes(x_range=[-1, PI], y_range=[-1, 4]).add_coordinates()
        
        f_graph = ax.plot(
            lambda x: x + np.sin(x),
            color=BLUE,
            x_range=[0, PI]
        )
        f_label = ax.get_graph_label(
            f_graph, r"y = x + \sin(x)", x_val=PI/2, direction=DR
        )

        k = ValueTracker(f_graph.t_min)
        
        moving_slope = always_redraw(
            lambda: ax.get_secant_slope_group(
                x = k.get_value(),
                graph = f_graph,
                dx = 0.05,
                secant_line_length = 10,
                secant_line_color = YELLOW
            )
        )
         
        # create dots based on the f_graph
        moving_dot = Dot(ax.i2gp(f_graph.t_min, f_graph), color=ORANGE)
        dot_1 = Dot(ax.i2gp(f_graph.t_min, f_graph))
        dot_2 = Dot(ax.i2gp(f_graph.t_max, f_graph))

        self.add(
            ax,
            f_graph, f_label,
            dot_1, dot_2, moving_dot,
            moving_slope
        )
        self.play(self.camera.frame.animate.scale(0.5).move_to(moving_dot))

        def update_curve(mob):
            mob.move_to(moving_dot.get_center())

        self.camera.frame.add_updater(update_curve)
        self.play(
            MoveAlongPath(moving_dot, f_graph, rate_func=there_and_back),
            k.animate.set_value(f_graph.t_max),
            rate_func=there_and_back,
            run_time=8
        )
        self.wait(2)
                          
        self.camera.frame.remove_updater(update_curve)
        self.play(Restore(self.camera.frame))
        
        self.camera.frame.add_updater(update_curve)
        self.play(
            MoveAlongPath(moving_dot, f_graph, rate_func=there_and_back),
            k.animate.set_value(f_graph.t_max),
            rate_func=there_and_back,
            run_time=8
        )
        self.wait(2)
        
        self.camera.frame.remove_updater(update_curve)
        self.play(Restore(self.camera.frame))
        
        self.wait(2)

        
# Question 3
class Bac2024Sujet0Exo5Question3(Scene):
    def construct(self):
        msg1 = "Bac 2024 Sujet 0 Exercice 5"
        title3 = Title(f"{msg1}")
        self.add(title3.scale(1))
        self.wait(2)

        question3 = Title("Question 3")
        q3_txt = [
            r"3. Une urne contient cinquant boules numérotées de 1 à 50. "
            r"On tire successivement trois boules dans cette urne, "
            r"sans remise.",
            r"On appelle tirage la liste non ordonnée des numéros "
            r"des trois boules tirées.",
            r"Quel est le nombre de tirages possibles, sans tenir "
            r"compte de l'ordre des numéros ?"
        ]
        q3 = [Tex(t).scale(0.75) for t in q3_txt]
        q3VGroup = VGroup(*q3)
        
        disp_tex_list(self, 
            previous_mobj=None,
            tex_list=q3,
            next2obj=title3,
            direction=DOWN
        )
        a = r"a. \(50^3\)"
        b = r"b. \(1\times 2\times 3\)"
        c = r"c. \(50\times 49\times 48\)"
        d = r"d. \(\dfrac{50\times 49\times 48}{1\times 2\times 3}\)"

        m1 = MobjectMatrix(
            [[Tex(a), Tex(b), Tex(c), Tex(d)]],
            v_buff=0.75,
            h_buff=5,
            left_bracket="\{",
            right_bracket="\}"
        ).scale(0.75)

        
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
        sol_d = ent[3]
        box_d = SurroundingRectangle(sol_d)
        solution3 = Title("Réponse d")
        self.play(
            ReplacementTransform(attention_rep, solution3),
            Write(box_d)
        )
        self.wait()

        
        explanation = Title("Explications")

        self.play(
            Unwrite(box_d),
            ReplacementTransform(solution3, explanation.scale(0.75))
        )
        self.wait()
        
        D00 = r"Il y a 50 choix pour le premier tirage, 49 pour le second et 48 pour le troisième."
        D01 = r"Ce qui fait \(50\times 49\times 48\) choix possibles..."
        D02 = r"Mais comme l'énoncé nous dit de ne pas tenir compte de l'ordre..."
        D03 = r"Alors il faut diviser par le nombre de permutations de 3 éléments."
        D04 = r"D'où le résultat : \(\dfrac{50\times 49\times 48}{1\times 2\times 3}\)"
        
        D = [D00, D01, D02, D03, D04]
        dD = [Tex(d).scale(0.75) for d in D]
        dDVGroup = VGroup(*dD)
        

        disp_tex_list(self, 
            previous_mobj=m1,
            tex_list=dD,
            next2obj=q3[-1],
            direction=DOWN
        )

        
        remark = [
            r"On peut remarquer que : \(\dfrac{50\times 49\times 48}{1\times 2\times 3} = \dfrac{50!}{3!47!}\)",
            r"C'est-à-dire \(\dfrac{50\times 49\times 48}{1\times 2\times 3} = \dfrac{50!}{3!(50 - 3)!}\)",
            r"Soit \(\dfrac{50\times 49\times 48}{1\times 2\times 3} = \binom{50}{3}\)",
            r"Ce qui signifie que choisir (simultanément) 3 éléments parmi 50 ",
            r"est équivalent à  effectuer trois tirages sans remise ",
            r"sans tenir compte de l'ordre."
        ]

        rem_tex = [Tex(r) for r in remark]

        erase_all = VGroup(q3VGroup, dDVGroup)
        
        disp_tex_list(self, 
            previous_mobj=erase_all,
            tex_list=rem_tex,
            next2obj=explanation,
            direction=DOWN
        )



import networkx as nx

class Tree(Scene):
    def construct(self):
        G = nx.Graph()

        G.add_node("ROOT")

        for i in range(5):
            # G.add_node("Child_%i" % i)
            # G.add_node("Grandchild_%i" % i)
            # G.add_node("Greatgrandchild_%i" % i)

            G.add_edge("ROOT", "Child_%i" % i)
            G.add_edge("Child_%i" % i, "Grandchild_%i" % i)
            G.add_edge("Grandchild_%i" % i, "Greatgrandchild_%i" % i)

        self.play(Create(
            Graph(list(G.nodes), list(G.edges), layout="tree", root_vertex="ROOT")))



class Bac2024Sujet0Exo5Question3Arbre(Scene):
    def construct(self):
        msg1 = "Bac 2024 Sujet 0 Exercice 5"
        title3 = Title(f"{msg1}")
        self.add(title3.scale(1))
        self.wait(2)

        illustration = Title(r"Illustration pour \(n = 3\) boules différentes")
        self.play(ReplacementTransform(title3, illustration))
        self.wait()
        
        
        vertices = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
        edges = [
            (0, 1), (0, 2), (0, 3),
            (1, 4), (1, 5),
            (2, 6), (2, 7),
            (3, 8), (3, 9),
            (4, 10),
            (5, 11),
            (6, 12),
            (7, 13),
            (8, 14),
            (9, 15)
        ]
        true_labels = {
            0:"0",
            1:"1", 2:"2", 3:"3",
            4:"2", 5:"3", 6:"1", 7:"3", 8:"1", 9:"2",
            10: "3", 11:"2", 12:"3", 13:"1", 14:"2", 15:"1"
        }

        vertices_colors = {
            0: {"color": YELLOW},
            1: {"color": BLUE}, 2: {"color": WHITE}, 3: {"color": RED},
            4: {"color": WHITE}, 5: {"color": RED}, 6: {"color": BLUE},
            7: {"color": RED}, 8: {"color" : BLUE}, 9: {"color": WHITE},
            10: {"color": RED}, 11: {"color": WHITE}, 12: {"color": RED},
            13: {"color": BLUE}, 14: {"color": WHITE}, 15: {"color": BLUE}
        }

        edges_colors = {
            (0, 1): {"stroke_color": BLUE},
            (0, 2): {"stroke_color": WHITE},
            (0, 3): {"stroke_color": RED},
            (1, 4): {"stroke_color": WHITE},
            (1, 5): {"stroke_color": RED},
            (2, 6): {"stroke_color": BLUE},
            (2, 7): {"stroke_color": RED},
            (3, 8): {"stroke_color": BLUE},
            (3, 9): {"stroke_color": WHITE},
            (4, 10): {"stroke_color": RED},
            (5, 11): {"stroke_color": WHITE},
            (6, 12): {"stroke_color": RED},
            (7, 13): {"stroke_color": BLUE},
            (8, 14): {"stroke_color": WHITE},
            (9, 15): {"stroke_color": BLUE},
        }

        
        
        g = Graph(
            vertices, edges, layout="tree", root_vertex=0,
            layout_scale=3, labels=true_labels, 
                  edge_config=edges_colors,
            vertex_config=vertices_colors,
        )

        tree_illustrate = Title("Avec un arbre")
        self.play(
            ReplacementTransform(illustration, tree_illustrate),
            Create(g)
        )
        self.wait(2)

        T_1 = (1, 4, 10) # un_deux_trois
        T_2 = (1, 5, 11) # un_trois_deux
        T_3 = (2, 6, 12) # deux_un_trois
        T_4 = (2, 7, 13) # deux_trois_un
        T_5 = (3, 8, 14) # trois_un_deux
        T_6 = (3, 9, 15) # trois_deux_un

        L_1 = [
            Tex(
                true_labels[t],
                color=vertices_colors[t]["color"]
            ) for t in T_1
        ]
        L_2 = [
            Tex(
                true_labels[t],
                color=vertices_colors[t]["color"]
            ) for t in T_2
        ]
        L_3 = [
            Tex(
                true_labels[t],
                color=vertices_colors[t]["color"]
            ) for t in T_3
        ]
        L_4 = [
            Tex(
                true_labels[t],
                color=vertices_colors[t]["color"]
            ) for t in T_4
        ]
        L_5 = [
            Tex(
                true_labels[t],
                color=vertices_colors[t]["color"]
            ) for t in T_5
        ]
        L_6 = [
            Tex(
                true_labels[t],
                color=vertices_colors[t]["color"]
            ) for t in T_6
        ]

        pos = [
            (g[10], g[11], g[12], g[13], g[14], g[15]),
            (0.5 * DOWN, 2.5 * DOWN, 4.5 * DOWN)
        ]
        self.play(
            *[Write(L_1[i].next_to(pos[0][0], pos[1][i])) for i in range(3)],
            # [L_1[i].animate.next_to(pos[0][0], pos[1][i]) for i in range(3)],
            # L_1[0].animate.next_to(pos[0][0], pos[1][0]),
            # L_1[1].animate.next_to(pos[0][0], pos[1][1]),
            # L_1[2].animate.next_to(pos[0][0], pos[1][2]),
            
        )
        self.wait()

        L_1VGroup = VGroup(*L_1)
        box_L_1 = SurroundingRectangle(L_1VGroup)
        self.play(Write(box_L_1))
        self.wait()
                  
        
        self.play(
            *[Write(L_2[i].next_to(pos[0][1], pos[1][i])) for i in range(3)],
        )
        self.wait()

        L_2VGroup = VGroup(*L_2)
        box_L_2 = SurroundingRectangle(L_2VGroup)
        self.play(Write(box_L_2))
        self.wait()
        
        self.play(
            *[Write(L_3[i].next_to(pos[0][2], pos[1][i])) for i in range(3)],
        )
        self.wait()

        L_3VGroup = VGroup(*L_3)
        box_L_3 = SurroundingRectangle(L_3VGroup)
        self.play(Write(box_L_3))
        self.wait()
        
        self.play(
            *[Write(L_4[i].next_to(pos[0][3], pos[1][i])) for i in range(3)],
        )
        self.wait()

        L_4VGroup = VGroup(*L_4)
        box_L_4 = SurroundingRectangle(L_4VGroup)
        self.play(Write(box_L_4))
        self.wait()

        self.play(
            *[Write(L_5[i].next_to(pos[0][4], pos[1][i])) for i in range(3)],
        )
        self.wait()
        
        L_5VGroup = VGroup(*L_5)
        box_L_5 = SurroundingRectangle(L_5VGroup)
        self.play(Write(box_L_5))
        self.wait()

        self.play(
            *[Write(L_6[i].next_to(pos[0][5], pos[1][i])) for i in range(3)],
        )
        self.wait()
        L_6VGroup = VGroup(*L_6)
        box_L_6 = SurroundingRectangle(L_6VGroup)
        self.play(Write(box_L_6))
        self.wait()
        
        boxes_L = [box_L_1, box_L_2, box_L_3, box_L_4, box_L_5, box_L_6]

        t0 = Table(
            [
                ["1", "2", "3", "1", "3", "2"],
                ["2", "1", "3", "2", "3", "1"],
                ["3", "1", "2", "3", "2", "1"],
            ]
        )

        # t0.add_highlighted_cell((1, 1), color=BLUE)
        # t0.add_highlighted_cell((1, 2), color=WHITE)
        # t0.add_highlighted_cell((1, 3), color=RED)
        # t0.add_highlighted_cell((1, 4), color=BLUE)
        # t0.add_highlighted_cell((1, 5), color=RED)
        # t0.add_highlighted_cell((1, 6), color=WHITE)

        # t0.add_highlighted_cell((2, 1), color=WHITE)
        # t0.add_highlighted_cell((2, 2), color=BLUE)
        # cell22 = t0.get_cell((2, 2), color=BLUE)
        # t0.add_highlighted_cell((2, 3), color=RED)
        # t0.add_highlighted_cell((2, 4), color=WHITE)
        # t0.add_highlighted_cell((2, 5), color=RED)
        # t0.add_highlighted_cell((2, 6), color=BLUE)

        # t0.add_highlighted_cell((3, 1), color=RED)
        # t0.add_highlighted_cell((3, 2), color=BLUE)
        # t0.add_highlighted_cell((3, 3), color=WHITE)
        # t0.add_highlighted_cell((3, 4), color=RED)
        # t0.add_highlighted_cell((3, 5), color=WHITE)
        # t0.add_highlighted_cell((3, 6), color=BLUE)

        ent = t0.get_entries()
        # table_colors = {
        #     0: {"color": BLUE}, 1: {"color": WHITE}, 2: {"color": RED},
        #     3: {"color": BLUE}, 4: {"color": RED}, 5: {"color": WHITE},
        #     6: {"color": WHITE}, 7: {"color": BLUE}, 8: {"color": RED},
        #     9: {"color": RED}, 10: {"color": BLUE}, 11: {"color": RED},
        #     12: {"color": RED}, 13: {"color": BLUE}, 14: {"color": WHITE},
        #     15: {"color": RED}, 16: {"color": WHITE}, 17: {"color": RED},
        # }
        table_colors = {
            0: BLUE, 1: WHITE, 2: RED,
            3: BLUE, 4: RED, 5: WHITE,
            6: WHITE, 7: BLUE, 8: RED,
            9: RED, 10: BLUE, 11: RED,
            12: RED, 13: BLUE, 14: WHITE,
            15: RED, 16: WHITE, 17: RED,
        }

        for i in range(len(ent)):
            ent[i].set_color(table_colors[i])

        sort1_H = SurroundingRectangle(ent[0:3])
        sort1_V = SurroundingRectangle(ent[0:3])
        
        sort2_H = SurroundingRectangle(ent[3:6])
        sort2_V = SurroundingRectangle(ent[3:6])
        
        sort3_H = SurroundingRectangle(ent[6:9])
        sort3_V = SurroundingRectangle(ent[6:9])
        
        sort4_H = SurroundingRectangle(ent[9:12])
        sort4_V = SurroundingRectangle(ent[9:12])
        
        sort5_H = SurroundingRectangle(ent[12:15])
        sort5_V = SurroundingRectangle(ent[12:15])
        
        sort6_H = SurroundingRectangle(ent[15:18])
        sort6_V = SurroundingRectangle(ent[15:18])
        
        sorts_H = [sort1_H, sort2_H, sort3_H, sort4_H, sort5_H, sort6_H]
        sorts_V = [sort1_V, sort2_V, sort3_V, sort4_V, sort5_V, sort6_V]

        table_illustrate = Title("Avec un tableau")
        self.play(
            ReplacementTransform(tree_illustrate, table_illustrate),
            ReplacementTransform(g, t0),
        )
        self.wait(2)

        
        self.play(
            Write(sort1_H)
        )
        # self.play(Write(ent[1].next_to(ent[0], RIGHT)))
        # self.play(Write(ent[2].next_to(ent[1], RIGHT)))
        # boxes = [SurroundingRectangle(ent[i:i+3]) for i in range(len(sorts)]
        # self.play(Write(boxes[0]))
        self.wait()

        for i in range(len(sorts_H) - 1):
            self.play(
                ReplacementTransform(sorts_V[i], boxes_L[i]),
                ReplacementTransform(sorts_H[i], sorts_H[i+1]),
                # Write(ent[i+3].next_to(ent[i+2], RIGHT)),
            )
            # self.play(Write(ent[i+4].next_to(ent[i+3], RIGHT)))
            # self.play(Write(ent[i+5].next_to(ent[i+4], RIGHT)))
            # boxes.append(SurroundingRectangle(ent[i+3:i+6]))
            self.wait()
        self.play(ReplacementTransform(sorts_H[-1], boxes_L[-1]))
        self.wait()

        remark = [
            r"Si on ne tient pas compte de l'ordre, ",
            r"tous ces tirages sont équivalents.",
            r"Il s'agit exactement du nombre de permutation de 3 éléments.",
        ]

        rem_tex = [Tex(r) for r in remark]
        remVGroup = VGroup(*rem_tex)
        
        disp_tex_list(self, 
            previous_mobj=t0,
            tex_list=rem_tex,
            next2obj=table_illustrate,
            direction=DOWN
        )

        s1, s2, s3 = [Square(color=YELLOW) for _ in range(3)]
        squares = VGroup(s1, s2, s3)

        perm = Title("Permutations")
        # self.play(*[Write(o) for o in [s1, s2, s3]])
        self.play(
            ReplacementTransform(table_illustrate, perm),
            ReplacementTransform(remVGroup, squares)
        )
        self.wait()
        
        # align squares next to one another
        self.play(
            s1.animate.next_to(s2, LEFT),
            s3.animate.next_to(s2, RIGHT)
        )

        # create numbers for each of them
        colors = [BLUE, WHITE, RED]
        nums = [Tex(f"\({i+1}\)", color=colors[i]).scale(3) for i in range(3)]
        t1, t2, t3 = nums
        
        t1.move_to(s1)
        t2.move_to(s2)
        t3.move_to(s3)

        self.play(
            *[Write(o) for o in nums],
            ReplacementTransform(boxes_L[0], s1),
            ReplacementTransform(boxes_L[1], s1),
            ReplacementTransform(boxes_L[2], s2),
            ReplacementTransform(boxes_L[3], s2),
            ReplacementTransform(boxes_L[4], s3),
            ReplacementTransform(boxes_L[5], s3),
        )
        self.wait()

        permutations3 = [L_1, L_2, L_3, L_4, L_5, L_6]
        L = permutations3
        for i in range(len(L)):
            if i == 1:
                self.play(
                    Swap(s2, s3),
                    Swap(t2, t3)
                )
                self.wait()
            elif i == 2:
                self.play(
                    Swap(s2, s1),
                    Swap(t2, t1)
                )
                self.wait()
                self.play(
                    Swap(s3, s1),
                    Swap(t3, t1)
                )
                self.wait()
            elif i == 3:
                self.play(
                    Swap(s3, s1),
                    Swap(t3, t1)
                )
                self.wait()
            elif i == 4:
                self.play(
                    Swap(s2, s3),
                    Swap(t2, t3)
                )
                self.wait()
                self.play(
                    Swap(s1, s2),
                    Swap(t1, t2)
                )
                self.wait()
            elif i == 5:
                self.play(
                    Swap(s1, s2),
                    Swap(t1, t2)
                )
                self.wait()

            self.play(
                *[ReplacementTransform(L[i][j], nums[j]) for j in range(3)]
            )
            self.wait()
        
                  
# Question 3 Généralisation de l'arbre
class Bac2024Sujet0Exo5Question3Trees(Scene):
    def construct(self):
        msg1 = "Bac 2024 Sujet 0 Exercice 5"
        title3 = Title(f"{msg1}")
        self.add(title3.scale(1))
        self.wait(2)

        
        generalize = Title("Vers une généralisation").scale(0.85)
        gen_txt = [
            r"Voyons ce qui se passe avec 4 boules au total.",
            r"On tire toujours 3 boules sans remise",
            r"et sans tenir compte de l'ordre.",
        ]
        gen = [Tex(r).scale(0.85) for r in gen_txt]
        genVGroup = VGroup(*gen)
        
        disp_tex_list(self, 
            previous_mobj=None,
            tex_list=gen,
            next2obj=title3,
            direction=DOWN
        )
        
        
        self.play(
            ReplacementTransform(title3, generalize),
        )

        vertices = list(range(41))
        edges = [
            # 1er tirage 4 possibilités
            (0, 1), (0, 2), (0, 3), (0, 4),
            # 2eme tirage 3 possibilités pour chacune des 4 options
            (1, 5), (1, 6), (1, 7), # (1, 2), (1, 3), (1, 4)
            (2, 8), (2, 9), (2, 10), # (2, 1), (2, 3), (2, 4)
            (3, 11), (3, 12), (3, 13), # (3, 1), (3, 2), (3, 4)
            (4, 14), (4, 15), (4, 16), # (4, 1), (4, 2), (4, 3)
            # 3ème tirage 2 possibilités pour chacune des 3 options
            # du 2nd tirage
            (5, 17), (5, 18), # (1, 2, 3), (1, 2, 4)
            (6, 19), (6, 20), # (1, 3, 4), (1, 3, 2)
            (7, 21), (7, 22), # (1, 4, 2), (1, 4, 3)
            (8, 23), (8, 24), # (2, 1, 4), (2, 1, 3)
            (9, 25), (9, 26), # (2, 3, 4), (2, 3, 1)
            (10, 27), (10, 28), # (2, 4, 1), (2, 4, 3)
            (11, 29), (11, 30), # (3, 1, 4), (3, 1, 2)
            (12, 31), (12, 32), # (3, 2, 1), (3, 2, 4)
            (13, 33), (13, 34), # (3, 4, 1), (3, 4, 2)
            (14, 35), (14, 36), # (4, 1, 2), (4, 1, 3)
            (15, 37), (15, 38), # (4, 2, 3), (4, 2, 1)
            (16, 39), (16, 40), # (4, 3, 1), (4, 3, 2)
        ]
        
        true_labels = {
            0:"D",
            1:"1", 2:"2", 3:"3", 4:"4",
            5:"2", 6:"3", 7:"4", 8:"1",
            9:"3", 10: "4", 11:"1", 12:"2",
            13:"4", 14:"1", 15:"2", 16:"3",
            17:"3", 18:"4", 19:"4", 20:"2",
            21:"2", 22:"3", 23:"4", 24:"3",
            25:"4", 26:"1", 27:"1", 28:"3",
            29:"4", 30:"2", 31:"1", 32:"4",
            33:"1", 34:"2", 35:"2", 36:"3",
            37:"3", 38:"1", 39:"1", 40:"2"
        }


        color_values = {
            "D": {"color": YELLOW},
            "1": {"color": BLUE},
            "2": {"color": WHITE},
            "3": {"color": RED},
            "4": {"color": PURPLE}
        }

        vertices_colors = {
            i : color_values[true_labels[i]] for i in range(41)
        }
        
        edges_colors = {
            edge : {
                "stroke_color": color_values[true_labels[edge[1]]]["color"]
            } for edge in edges
        }
        
        g = Graph(
            vertices, edges, layout="tree", root_vertex=0,
            layout_scale=6, labels=True,#true_labels, 
                  # edge_config=edges_colors,
            # vertex_config=vertices_colors,
            layout_config={
                "vertex_spacing" : (0.75, 1.75),
            }
        )

        self.play(
            FadeOut(genVGroup),
            Create(g.next_to(generalize, 0.25 * DOWN).scale(0.75)),
            g.animate.shift(UP)
        )
        self.wait(2)


        T_1 = (1, 5, 17) # 
        T_2 = (1, 5, 18) # 
        T_3 = (1, 6, 19) # 
        T_4 = (1, 6, 20) # 
        T_5 = (1, 7, 21) # 
        T_6 = (1, 7, 22) # 
        T_7 = (2, 8, 23) # 
        T_8 = (2, 8, 24) # 
        T_9 = (2, 9, 25) # 
        T_10 = (2, 9, 26) #
        T_11 = (2, 10, 27) # 
        T_12 = (2, 10, 28) # 
        T_13 = (3, 11, 29) # 
        T_14 = (3, 11, 30) # 
        T_15 = (3, 12, 31) # 
        T_16 = (3, 12, 32) #
        T_17 = (3, 13, 33) #
        T_18 = (3, 13, 34) # 
        T_19 = (4, 14, 35) #
        T_20 = (4, 14, 36) #
        T_21 = (4, 15, 37) #
        T_22 = (4, 15, 38) #
        T_23 = (4, 16, 39) #
        T_24 = (4, 16, 40) # 
        
        T = [
            T_1, T_2, T_3, T_4, T_5, T_6, T_7, T_8,
            T_9, T_10, T_11, T_12, T_13, T_14, T_15, T_16,
            T_17, T_18, T_19, T_20, T_21, T_22, T_23, T_24
        ]

    
        L = [
            [
                Tex(
                    true_labels[t],
                    color=vertices_colors[t]["color"]
                ) for t in T_i
            ] for T_i in T
        ]


        pos = [
            [g[i] for i in range(17, 41)],
            (0.5 * DOWN, 2.5 * DOWN, 4.5 * DOWN)
        ]        
        for i in range(len(L)):
            self.play(
                *[
                    Write(
                        L[i][j].next_to(
                            pos[0][i],
                            pos[1][j]
                        )
                    ) for j in range(3) 
                ]
            )
            #self.wait()

        L_VGroups = [VGroup(*L_i) for L_i in L]
        boxes_L = [
            SurroundingRectangle(
                VGroup(*L_i),
                color=GREEN,
                corner_radius=0.2
            ) for L_i in L
        ]

        
        blocks = [VGroup(*L_VGroups[i:i+6]) for i in range(19)]
        block_boxes = [SurroundingRectangle(b) for b in blocks]
        
        self.play(Write(block_boxes[0]))
        self.wait()

        tree_1 = VGroup(
            g[1], g[5], g[6], g[7],
            g[17], g[18], g[19],
            g[20], g[21], g[22]
        )
        
        tree_1_box = SurroundingRectangle(tree_1)
        self.play(Write(tree_1_box))
        self.wait()

        def fadeout_doubles(self, boxes, lists):
            for i in range(3):
                self.play(
                    *[Write(b) for b in [boxes[i], boxes[i + 3]]],
                )
                self.wait()

                self.play(
                    ReplacementTransform(boxes[i+3], boxes[i]),
                    *[FadeOut(o) for o in lists[i+3]],
                    Unwrite(boxes[i]),
                )
                self.wait()
            
        fadeout_doubles(self, boxes=boxes_L, lists=L)    
        
        
        
class Bac2024Sujet0Exo5Question3Formule(Scene):
    def construct(self):
        msg1 = "Bac 2024 Sujet 0 Exercice 5"
        title3 = Title(f"{msg1}")
        self.add(title3.scale(1))
        self.wait(2)

        
        formula = Title("Formule générale")
        self.play(
            ReplacementTransform(title3, formula),
        )
        self.wait()
        
        f_txt = [
            r"Avec \(n\) objets distincts "
            r"et \(p\) tirages sans remises on a :",
            r"\(n\) possibilités au premier tirage ; ",
            r"\(n - 1\) possibilités au second tirage ; ",
            r"\(n - 2\) possibilités au troisième tirage ; ",
            r"\(n - p + 1\) possibilités au \(p\)-ème tirage.",
            r"Ainsi, d'après le principe multiplicatif, on a : ",
            r"\(n\times (n - 1)\times\dots\times (n - p + 1) = \dfrac{n!}{(n - p)!}\)",
            r"tirages distincts en tenant compte de l'ordre."
        ]
        f_tex = [Tex(f) for f in f_txt]
        

        disp_tex_list(self, 
            previous_mobj=None,
            tex_list=f_tex,
            next2obj=formula,
            direction=DOWN
        )

        
        
# Question 4
class Bac2024Sujet0Exo5Question4(Scene):
    def construct(self):
        msg1 = "Bac 2024 Sujet 0 Exercice 5"
        title4 = Title(f"{msg1}")
        self.add(title4.scale(1))
        self.wait(2)

        
        question4 = Title("Question 4").scale(0.85)
        q4_txt = [
            r"4. On effectue dix lancers d'une pièce de monnaie. ",
            r"Le résultat d'un lancer est pile ou face.",
            r"On note la liste ordonnée des dix résultats.",
            r"Quel est le nombre de listes ordonnées possibles ?",
        ]
        q4 = [Tex(r).scale(0.85) for r in q4_txt]

        disp_tex_list(self, 
            previous_mobj=None,
            tex_list=q4,
            next2obj=title4,
            direction=DOWN
        )
        
        a = r"a. \(2\times 10\)"
        b = r"b. \(2^{10}\)"
        c = r"c. \(1\times 2\times 3\times\dots \times 10\)"
        d = r"d. \(\dfrac{1\times 2\times 3\times\dots \times 10}{1\times 2}\)"
        
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
        sol_b = ent[1]
        box_b = SurroundingRectangle(sol_b)
        solution4 = Title("Réponse b")
        self.play(
            ReplacementTransform(attention_rep, solution4),
            Write(box_b)
        )
        self.wait()

        
        explanation = Title("Explications")
        self.play(
            ReplacementTransform(solution4, explanation),
            Unwrite(box_b)
        )
        self.wait()

        
        exp_b = [
            r"Le mot ordonnée indique simplement qu'on tient compte ",
            r"toutes les listes (même si elles ont le même nombre de pile).",
            r"Ça veut juste dire qu'on compte toutes les feuilles de l'arbre.",
            r"Chaque branche engendre 2 nouvelles branches.",
            r"1er tirage : 2 branches, 2e tirage : 4 branches, 3e : 8 branches...",
            r"10e tirage : \(2^{10}\) branches.",
        ]

        b_tex = [Tex(r).scale(0.85) for r in exp_b]
        disp_tex_list(self, 
            previous_mobj=m1,
            tex_list=b_tex,
            next2obj=q4[-1],
            direction=DOWN
        )
        


class Bac2024Sujet0Exo5Question4Arbre(Scene):
    def construct(self):
        msg1 = "Bac 2024 Sujet 0 Exercice 5"
        title4 = Title(f"{msg1}")
        self.add(title4.scale(1))
        self.wait(2)

        illustration = Title(r"Illustration pour \(n = 4\) lancers")
        self.play(ReplacementTransform(title4, illustration))
        self.wait()
        
        
        vertices = list(range(31))
        edges = [
            (0, 1), (0, 2), 
            (1, 3), (1, 4), (2, 5), (2, 6),
            (3, 7), (3, 8), (4, 9), (4, 10), (5, 11), (5, 12), (6, 13), (6, 14),
            (7, 15),(7, 16), (8, 17), (8, 18), (9, 19), (9, 20), (10, 21), (10, 22), (11, 23), (11, 24), (12, 25), (12, 26), (13, 27), (13, 28), (14, 29), (14, 30), 
        ]
        
        true_labels = {
            0:"L",
            1:"P", 2:"F",
            3:"P", 4:"F", 5:"P", 6:"F",
            7:"P", 8:"F", 9:"P", 10: "F", 11:"P", 12:"F", 13:"P", 14:"F",
            15:"P", 16:"F", 17:"P", 18:"F", 19:"P", 20:"F", 21:"P", 22:"F", 23:"P", 24:"F", 25:"P", 26:"F", 27:"P", 28:"F", 29:"P", 30:"F", 
        }

        vertices_colors = {
            0: {"color": YELLOW},
            1: {"color": RED}, 2: {"color": GREEN},
            3: {"color": RED}, 4: {"color": GREEN},
            5: {"color": RED}, 6: {"color": GREEN},
            7: {"color": RED}, 8: {"color" : GREEN},
            9: {"color": RED}, 10: {"color": GREEN},
            11: {"color": RED}, 12: {"color": GREEN},
            13: {"color": RED}, 14: {"color": GREEN},
            15: {"color": RED}, 16: {"color": GREEN},
            17: {"color": RED}, 18: {"color": GREEN},
            19: {"color": RED}, 20: {"color": GREEN},
            21: {"color": RED}, 22: {"color": GREEN},
            23: {"color": RED}, 24: {"color": GREEN},
            25: {"color": RED}, 26: {"color": GREEN},
            27: {"color": RED}, 28: {"color": GREEN},
            29: {"color": RED}, 30: {"color": GREEN},
        }

        edges_colors = {
            (0, 1):{"stroke_color": RED},
            (0, 2): {"stroke_color": GREEN}, 
            (1, 3): {"stroke_color": RED},
            (1, 4): {"stroke_color": GREEN},
            (2, 5): {"stroke_color": RED},
            (2, 6): {"stroke_color": GREEN},
            (3, 7): {"stroke_color": RED},
            (3, 8): {"stroke_color": GREEN},
            (4, 9): {"stroke_color": RED},
            (4, 10): {"stroke_color": GREEN},
            (5, 11): {"stroke_color": RED},
            (5, 12): {"stroke_color": GREEN},
            (6, 13): {"stroke_color": RED},
            (6, 14): {"stroke_color": GREEN},
            (7, 15): {"stroke_color": RED},
            (7, 16): {"stroke_color": GREEN},
            (8, 17): {"stroke_color": RED},
            (8, 18): {"stroke_color": GREEN},
            (9, 19): {"stroke_color": RED},
            (9, 20): {"stroke_color": GREEN},
            (10, 21): {"stroke_color": RED},
            (10, 22): {"stroke_color": GREEN},
            (11, 23): {"stroke_color": RED},
            (11, 24): {"stroke_color": GREEN},
            (12, 25): {"stroke_color": RED},
            (12, 26): {"stroke_color": GREEN},
            (13, 27): {"stroke_color": RED},
            (13, 28): {"stroke_color": GREEN},
            (14, 29): {"stroke_color": RED},
            (14, 30): {"stroke_color": GREEN}, 
        }

        
        
        g = Graph(
            vertices, edges, layout="tree", root_vertex=0,
            layout_scale=6.65, labels=true_labels, 
                  edge_config=edges_colors,
            vertex_config=vertices_colors,
        )

        tree_illustrate = Title("Avec un arbre")
        self.play(
            ReplacementTransform(illustration, tree_illustrate),
            Create(g)
        )
        self.wait(2)

        binary_labels = {
            0:"L",
            1:"0", 2:"1",
            3:"0", 4:"1", 5:"0", 6:"1",
            7:"0", 8:"1", 9:"0", 10: "1", 11:"0", 12:"1", 13:"0", 14:"1",
            15:"0", 16:"1", 17:"0", 18:"1", 19:"0", 20:"1", 21:"0", 22:"1", 23:"0", 24:"1", 25:"0", 26:"1", 27:"0", 28:"1", 29:"0", 30:"1", 
        }

        g_binary = Graph(
            vertices, edges, layout="tree", root_vertex=0,
            layout_scale=6.65, labels=True, #binary_labels, 
                  edge_config=edges_colors,
            vertex_config=vertices_colors,
        )

        binary_tree = Title("Codons \(P = 0\) et \(F = 1\)")
        self.play(
            ReplacementTransform(tree_illustrate, binary_tree),
            ReplacementTransform(g, g_binary)
        )
        self.wait(2)

        T_1 = (1, 3, 7, 15) # PPPP
        T_2 = (1, 3, 7, 16) # PPPF
        T_3 = (1, 3, 8, 17) # PPFP
        T_4 = (1, 3, 8, 18) # PPFF
        T_5 = (1, 4, 9, 19) # PFPP
        T_6 = (1, 4, 9, 20) # PFPF
        T_7 = (1, 4, 10, 21) # PFFP
        T_8 = (1, 4, 10, 22) # PFFF
        T_9 = (2, 5, 11, 23) # FPPP
        T_10 = (2, 5, 11, 24) # FPPF
        T_11 = (2, 5, 12, 25) # FPFP
        T_12 = (2, 5, 12, 26) # FPFF
        T_13 = (2, 6, 13, 27) # FFPP
        T_14 = (2, 6, 13, 28) # FFPF
        T_15 = (2, 6, 14, 29) # FFFP
        T_16 = (2, 6, 14, 30) # FFFF

        T = [
            T_1, T_2, T_3, T_4, T_5, T_6, T_7, T_8,
            T_9, T_10, T_11, T_12, T_13, T_14, T_15, T_16,
        ]

        

        L = []
        L = [
            L.append(
                [
                    Tex(
                        binary_labels[t],
                        color=vertices_colors[t]["color"]
                    ) for t in Ti
                ]) for Ti in T
        ]
        # L_1 = [
        #     Tex(
        #         true_labels[t],
        #         color=vertices_colors[t]["color"]
        #     ) for t in T_1
        # ]
        # L_2 = [
        #     Tex(
        #         true_labels[t],
        #         color=vertices_colors[t]["color"]
        #     ) for t in T_2
        # ]
        # L_3 = [
        #     Tex(
        #         true_labels[t],
        #         color=vertices_colors[t]["color"]
        #     ) for t in T_3
        # ]
        # L_4 = [
        #     Tex(
        #         true_labels[t],
        #         color=vertices_colors[t]["color"]
        #     ) for t in T_4
        # ]
        # L_5 = [
        #     Tex(
        #         true_labels[t],
        #         color=vertices_colors[t]["color"]
        #     ) for t in T_5
        # ]
        # L_6 = [
        #     Tex(
        #         true_labels[t],
        #         color=vertices_colors[t]["color"]
        #     ) for t in T_6
        # ]

        # pos = [
        #     (g[10], g[11], g[12], g[13], g[14], g[15]),
        #     (0.5 * DOWN, 2.5 * DOWN, 4.5 * DOWN)
        # ]
        # self.play(
        #     *[Write(L_1[i].next_to(pos[0][0], pos[1][i])) for i in range(3)],
        #     # [L_1[i].animate.next_to(pos[0][0], pos[1][i]) for i in range(3)],
        #     # L_1[0].animate.next_to(pos[0][0], pos[1][0]),
        #     # L_1[1].animate.next_to(pos[0][0], pos[1][1]),
        #     # L_1[2].animate.next_to(pos[0][0], pos[1][2]),
            
        # )
        # self.wait()

        # L_1VGroup = VGroup(*L_1)
        # box_L_1 = SurroundingRectangle(L_1VGroup)
        # self.play(Write(box_L_1))
        # self.wait()
                  
        
        # self.play(
        #     *[Write(L_2[i].next_to(pos[0][1], pos[1][i])) for i in range(3)],
        # )
        # self.wait()

        # L_2VGroup = VGroup(*L_2)
        # box_L_2 = SurroundingRectangle(L_2VGroup)
        # self.play(Write(box_L_2))
        # self.wait()
        
        # self.play(
        #     *[Write(L_3[i].next_to(pos[0][2], pos[1][i])) for i in range(3)],
        # )
        # self.wait()

        # L_3VGroup = VGroup(*L_3)
        # box_L_3 = SurroundingRectangle(L_3VGroup)
        # self.play(Write(box_L_3))
        # self.wait()
        
        # self.play(
        #     *[Write(L_4[i].next_to(pos[0][3], pos[1][i])) for i in range(3)],
        # )
        # self.wait()

        # L_4VGroup = VGroup(*L_4)
        # box_L_4 = SurroundingRectangle(L_4VGroup)
        # self.play(Write(box_L_4))
        # self.wait()

        # self.play(
        #     *[Write(L_5[i].next_to(pos[0][4], pos[1][i])) for i in range(3)],
        # )
        # self.wait()
        
        # L_5VGroup = VGroup(*L_5)
        # box_L_5 = SurroundingRectangle(L_5VGroup)
        # self.play(Write(box_L_5))
        # self.wait()

        # self.play(
        #     *[Write(L_6[i].next_to(pos[0][5], pos[1][i])) for i in range(3)],
        # )
        # self.wait()
        # L_6VGroup = VGroup(*L_6)
        # box_L_6 = SurroundingRectangle(L_6VGroup)
        # self.play(Write(box_L_6))
        # self.wait()
        
        # boxes_L = [box_L_1, box_L_2, box_L_3, box_L_4, box_L_5, box_L_6]


# Question 5
class Bac2024Sujet0Exo5Question5(Scene):
    def construct(self):
        msg1 = "Bac USA 28 mars 2023 Sujet 2 Exercice 4"
        title5 = Title(f"{msg1}")
        self.add(title5.scale(1))
        self.wait(2)

        

        question5 = Title("Question 5").scale(0.55)
        q5_00 = r"5. On considère variable aléatoire \(X\) "
        q5_00 += r"suivant la loi binomiale \(\mathcal{B}(3; p)\)."
        q5_01 = r"On sait que \(P(X = 0) = \frac{1}{125}.\)"
        q5_02 = r"On peut affirmer que : "
        q5_txt = [q5_00, q5_01, q5_02]
        q5 = [Tex(r).scale(0.55) for r in q5_txt]

        disp_tex_list(self, 
            previous_mobj=None,
            tex_list=q5,
            next2obj=title5,
            direction=DOWN
        )
        
        a = r"a. \(p = \frac{1}{5}\)"
        b = r"b. \(P(X = 1) = \frac{124}{125}\)"
        c = r"c. \(p = \frac{4}{5}\)"
        d = r"d. \(P(X = 1) = \frac{4}{5}\)"
        
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
        aRight01 = r"On en déduit que \(p = \frac{1}{5}\)."

        aRight = [aRight00, aRight01]
        Ar = [Tex(r).scale(0.6) for r in aRight]
        disp_calculations(self, 
            previous_mobj=None,
            calcs=Ar,
            next2obj=m1,
            direction=DOWN
            )


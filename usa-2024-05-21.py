from manim import *
import manim
from math import e, pi
import math
from PIL import Image

def disp_sub(self, lang):
    if lang.lower() == "en":
        written, phon = "Subscribe", "/səbˈskraɪb/"
        svg_path = "/Users/digitalnomad/Documents/pics/svg/subscribe.svg"
        sub_pic = SVGMobject(svg_path)
        sub_scale = 0.8 
    elif lang.lower() == "fr":
        written, phon = "Abonnez-vous", "/abɔne vu/"
        png_path = "/Users/digitalnomad/Documents/pics/png/sabonner.png"
        sub_pic = ImageMobject(png_path)
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
# Bac 2024 Amérique du Nord 21 Mai 2024
##################################################

# Exo 1 Intro
class USA2024Exo1Intro(Scene):
    def construct(self):
        msg1 = "Bac 2024 Amérique du Nord 21 Mai 2024"
        title1 = Title(f"{msg1}")
        self.add(title1.scale(1))
        self.wait(2)

        my_template = TexTemplate()
        my_template.add_to_preamble(r"\usepackage{babel}")
        
        intro = [
            r"Un jeu vidéo récompense par un objet tiré au sort les joueurs ",
            r"""ayant remporté un défi. L'objet tiré peut être ``commun" ou """,
            r"""``rare". Deux types d'objets communs ou rares sont """,
            r"disponibles, des épées et des boucliers.",
            r"Les concepteurs du jeu vidéo ont prévu que :",
        ]
        intro_tex = [
            Tex(t, tex_template=my_template).scale(0.8) for t in intro
        ]
        disp_tex_list(self, 
            previous_mobj=None,
            tex_list=intro_tex,
            next2obj=title1,
            direction=DOWN
        )

        item1 = r"la probabilité de tirer un objet rare est de 7\%"
        item2 = r"si on tire un objet rare, la probabilité que ce soit "
        item2 += r"une épée est de 80\%"
        item3 = r"si on tire un objet commun, la probabilité que ce soit "
        item3 += r"épée est de 40\%"
        blist = BulletedList(item1, item2, item3, height=10, width=12)
        self.play(
            Write(blist.next_to(intro_tex[-1], DOWN))
        )
        self.wait()
        inde = Text("Les parties A et B sont indépendantes.", slant=ITALIC)
        self.play(Write(inde.next_to(blist, DOWN)))
        self.wait()
        
# Exo 1 Partie A Question 1
class USA2024Exo1PartAQ1(Scene):
    def construct(self):
        msg1 = "Bac 2024 Amérique du Nord 21 Mai 2024"
        title1 = Title(f"{msg1}")
        self.add(title1.scale(1))
        self.wait(2)

        my_template = TexTemplate()
        my_template.add_to_preamble(r"\usepackage{babel}")

        partA = Title("Partie A")
        self.play(
            ReplacementTransform(title1, partA)
        )
        
        intro = [
            r"Un joueur vient de remporter un défi et tire au sort un objet.",
            r"On note :",
        ]
        intro_tex = [Tex(t) for t in intro]
        disp_tex_list(self, 
            previous_mobj=None,
            tex_list=intro_tex,
            next2obj=partA,
            direction=DOWN
        )

        item1 = r"""R l'événement ``le joueur tire un objet rare" """
        item2 = r""" E l'événement ``le joueur tire une épée" """
        item3 = r"\(\overline{R}\) et \(\overline{E}\) les événements"
        item3 += r" contraires des événements R et E."
        blist = BulletedList(item1, item2, item3, height=10, width=12)
        self.play(
            Write(blist.next_to(intro_tex[-1], DOWN))
        )
        self.wait()

        q1 = [
            r"1. Dresser un arbre de pondéré modélisant la situation, ",
            r"puis calculer \(P(R\cap E)\)."
        ]
        q1_tex = [Tex(t) for t in q1]
        disp_tex_list(self, 
            previous_mobj=None,
            tex_list=q1_tex,
            next2obj=blist,
            direction=DOWN
        )


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


# Exo 1 Partie A Réponse 1
class USA2024Exo1PartAR1(Scene):
    def construct(self):
        msg1 = "Bac 2024 Amérique du Nord 21 Mai 2024"
        title3 = Title(f"{msg1}")
        self.add(title3.scale(1))
        self.wait(2)

        illustration = Title(r"Arbre pondéré")
        self.play(ReplacementTransform(title3, illustration))
        self.wait()
        
        
        vertices = [0, 1, 2, 3, 4, 5, 6]
        edges = [
            (0, 1), (0, 2), # Rare ou commun
            (1, 3), (1, 4), # Rare et épée ou Rare et bouclier
            (2, 5), (2, 6), # Commun et épée ou Commun et bouclier
        ]

        probas = [7, 93, 80, 20, 40, 60]
        probas_labels = [
            r"P(R) = ",
            r"P(\overline{R}) = ",
            r"P_R(E) = ",
            r"P_R(\overline{E}) = ",
            r"P_{\overline{R}}(E) = ",
            r"P_{\overline{R}}(\overline{E}) = "
        ]
        probas_tex = [
            MathTex(
                f"{probas_labels[i]}" +
                f"{probas[i]}" +
                r"\%"
            ).scale(0.75) for i in range(len(probas))
        ]
        probas_pos = [RIGHT, LEFT]
        
        true_labels = {
            0 : "D",
            1 : "R", 2 : Tex(r"\(\overline{R}\)"),
            3 : "E", 4 : Tex(r"\(\overline{E}\)"),
            5 : "E", 6 : Tex(r"\(\overline{E}\)"),
        }

        vertices_colors = {
            0: {"color": WHITE},
            1: {"color": GOLD}, 2: {"color": RED},
            3: {"color": GREEN},4: {"color": PURE_BLUE},
            5: {"color": GREEN}, 6: {"color": PURE_BLUE},
        }

        edges_colors = {
            (0, 1): {"stroke_color": GOLD},
            (0, 2): {"stroke_color": RED},
            (1, 3): {"stroke_color": GREEN},
            (1, 4): {"stroke_color": PURE_BLUE},
            (2, 5): {"stroke_color": GREEN},
            (2, 6): {"stroke_color": PURE_BLUE},
        }

        
        
        g = Graph(
            vertices, edges, layout="tree", root_vertex=0,
            layout_scale=4.5,
            layout_config={
                "vertex_spacing" : (3.5, 2.5),
            },
            labels=true_labels, 
            edge_config=edges_colors,
            vertex_config=vertices_colors,
        )

        
        probas_on_tree = []
        for i, edge in enumerate(edges):
            v1, v2 = edge
            vertex1_pos = g[v1].get_center()
            vertex2_pos = g[v2].get_center()
            edge_center = (vertex1_pos + vertex2_pos) / 2
            probas_on_tree.append(
                probas_tex[i].next_to(
                    edge_center,
                    probas_pos[i % 2]
                )
            )


        self.play(
            Create(g),
            *[Write(p) for p in probas_on_tree]
        )
        self.wait(2)

        pre = [
            r"P(R\cap E) = P(R)\times P_R(E)",
            r"P(R\cap E) = 0,07\times 0,8",
            r"P(R\cap E) = 0,56",
            r"P(R\cap E) = 56\%",
        ]
        pre_tex = [MathTex(pr) for pr in pre]
        disp_calculations(
            self,
            previous_mobj=None,
            calcs=pre_tex,
            next2obj=g[3],
            direction=DOWN
        )

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
        msg1 = "Bac 2024 Amérique du Nord 21 Mai 2024"
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
        msg1 = "Bac 2024 Amérique du Nord 21 Mai 2024"
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
            G.add_edge("ROOT", "Child_%i" % i)
            G.add_edge("Child_%i" % i, "Grandchild_%i" % i)
            G.add_edge("Grandchild_%i" % i, "Greatgrandchild_%i" % i)

        self.play(Create(
            Graph(list(G.nodes), list(G.edges), layout="tree", root_vertex="ROOT")))



                  
# Question 3 Généralisation de l'arbre
class Bac2024Sujet0Exo5Question3Trees(Scene):
    def construct(self):
        msg1 = "Bac 2024 Amérique du Nord 21 Mai 2024"
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
        
        #      1               2               3               4
        # 2    3    4     3    4    1     4    1    2     1    2    3
        #3 4  4 2  2 3   4 1  1 3  3 4   1 2  2 4  4 1   2 3  3 1  1 2

        true_labels = {
            #
            # Level 0: Start
            #
            0:"S", 

            #
            # Level 1: First Draw
            #      1               2               3               4
            1:"4", 2:"3", 3:"2", 4:"1",

            #
            # Level 2: Second Draw
            #      1               2               3               4
            # 2    3    4     3    4    1     4    1    2     1    2    3
            
            # 4's children (4, ?)
            5:"3", 6:"2", 7:"1",
            
            # 3's children (3, ?)
            8:"2", 9:"1", 10: "4",
            
            # 2's children (2, ?)
            11:"1", 12:"4", 13:"3",
            
            # 1's children (1, ?)
            14:"4", 15:"3", 16:"2",

            #
            # Level 3: Third Draw
            #      1               2               3               4
            # 2    3    4     3    4    1     4    1    2     1    2    3
            #3 4  4 2  2 3   4 1  1 3  3 4   1 2  2 4  4 1   2 3  3 1  1 2
    
            # 3's children (4, 3, ?)
            17:"2", 18:"1",
            # 2's children (4, 2, ?)
            19:"1", 20:"3",
            # 1's children (4, 1, ?)
            21:"3", 22:"2",

            # 2's children (3, 2, ?)
            23:"1", 24:"4",
            # 1's children (3, 1, ?)
            25:"4", 26:"2",
            # 4's children (3, 4, ?)
            27:"2", 28:"1",
            
            # 1's children (2, 1, ?)
            29:"4", 30:"3",
            # 4's children (2, 4, ?)
            31:"3", 32:"1",
            # 3's children (2, 3, ?)
            33:"1", 34:"4",

            # 4's children (1, 4, ?)
            35:"3", 36:"2",
            # 3's children (1, 3, ?)
            37:"2", 38:"4",
            # 2's children (1, 2, ?)
            39:"4", 40:"3"
        }


        color_values = {
            "S": {"color": YELLOW},
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
            layout_scale=6, labels=true_labels, 
                  edge_config=edges_colors,
            vertex_config=vertices_colors,
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


        # Level 1 = 1
        
        # Level 2 = 2 (1, 2, ?)
        T_1 = (4, 16, 40) # (1, 2, 3)
        T_2 = (4, 16, 39) # (1, 2, 4)

        # Level 2 = 3 (1, 2, ?)
        T_3 = (4, 15, 38) # (1, 3, 4)
        T_4 = (4, 15, 37) # (1, 3, 2)

        # Level 2 = 4 (1, 4, ?)
        T_5 = (4, 14, 36) # (1, 4, 2)
        T_6 = (4, 14, 35) # (1, 4, 3)

        
        # Level 1 = 2

        # Level 2 = 3 (2, 3, ?)
        T_7 = (3, 13, 34) # (2, 3, 4)
        T_8 = (3, 13, 33) # (2, 3, 1)

        # Level 2 = 4 (2, 4, ?)
        T_9 = (3, 12, 32)  # (2, 4, 1)
        T_10 = (3, 12, 31) # (2, 4, 3)

        # Level 2 = 1 (2, 1, ?)
        T_11 = (3, 11, 30) # (2, 1, 3)
        T_12 = (3, 11, 29) # (2, 1, 4)

        
        # Level 1 = 3

        # Level 2 = 4 (3, 4, ?)
        T_13 = (2, 10, 28) # (3, 4, 1)
        T_14 = (2, 10, 27) # (3, 4, 2)

        # Level 2 = 1 (3, 1, ?)
        T_15 = (2, 9, 26) # (3, 1, 2)
        T_16 = (2, 9, 25) # (3, 1, 4)

        # Level 2 = 2 (3, 2, ?)
        T_17 = (2, 8, 24) # (3, 2, 4)
        T_18 = (2, 8, 23) # (3, 2, 1)

        
        # Level 1 = 4

        # Level 2 = 1 (4, 1, ?)
        T_19 = (1, 7, 22) # (4, 1, 2)
        T_20 = (1, 7, 21) # (4, 1, 3)

        # Level 2 = 2 (4, 2, ?)
        T_21 = (1, 6, 20) # (4, 2, 3)
        T_22 = (1, 6, 19) # (4, 2, 1)

        # Level 2 = 3 (4, 3, ?)
        T_23 = (1, 5, 18) # (4, 3, 1)
        T_24 = (1, 5, 17) # (4, 3, 2)
        
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
            [g[i] for i in range(40, 16, -1)],
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

        
        blocks = [VGroup(*L_VGroups[i:i+6]) for i in range(0, 19, 6)]
        block_boxes = [SurroundingRectangle(b) for b in blocks]
        
        subtree_1 = VGroup(
            g[4],
            g[16], g[15], g[14],
            g[40], g[39],
            g[38], g[37],
            g[36], g[35]
        )
        subtree_1_box = SurroundingRectangle(subtree_1)
        
        subtree_2 = VGroup(
            g[3],
            g[13], g[12], g[11],
            g[34], g[33],
            g[32], g[31],
            g[30], g[29]
        )
        subtree_2_box = SurroundingRectangle(subtree_2)

        
        subtree_3 = VGroup(
            g[2],
            g[10], g[9], g[8],
            g[28], g[27],
            g[26], g[25],
            g[24], g[23]
        )
        subtree_3_box = SurroundingRectangle(subtree_3)
        
        subtree_4 = VGroup(
            g[1],
            g[7], g[6], g[5],
            g[22], g[21],
            g[20], g[19],
            g[18], g[17]
        )
        
        subtree_4_box = SurroundingRectangle(subtree_4) 
        
        subtrees = [subtree_1, subtree_2, subtree_3, subtree_4]
        subtrees_boxes = [
            subtree_1_box, subtree_2_box,
            subtree_3_box, subtree_4_box
        ]
        
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


        self.play(
            *[Write(o) for o in [block_boxes[0], subtrees_boxes[0]]]
        )
        self.wait()
        fadeout_doubles(self, boxes=boxes_L, lists=L)    
        
        for i in range(3):
            self.play(
                ReplacementTransform(block_boxes[i], block_boxes[i+1]),
                ReplacementTransform(subtrees_boxes[i], subtrees_boxes[i+1]),
            )
            self.wait()

            fadeout_doubles(
                self,
                boxes=boxes_L[(i+1) * 6:],
                lists=L[(i+1) * 6:]
            )    

        self.play(
            *[FadeOut(o) for o in [block_boxes[-1], subtrees_boxes[-1]]]
        )
        self.wait()

        boxes_L = [
            SurroundingRectangle(
                VGroup(*L_i),
                color=GREEN,
                corner_radius=0.2
            ) for L_i in L
        ]

        def fadeout_irregular_doubles(self, triplets, boxes, LVGroups):
            i_0, i_1, i_2 = triplets
            self.play(
                *[Write(boxes_L[i]) for i in triplets]
            )
            self.wait()

            self.play(
                *[ReplacementTransform(
                    boxes[i],
                    boxes[i_0]
                ) for i in {i_1, i_2}
                  ],
                *[FadeOut(LVGroups[i]) for i in {i_1, i_2}]
            )
            self.wait()

            self.play(FadeOut(boxes[i_0]))
            self.wait()

        triplets_of_doubles = [
            [0, 7, 14], [1, 8, 18], [2, 12, 19], [6, 13, 20]
        ]

        for tod in triplets_of_doubles:
            fadeout_irregular_doubles(
                self,
                triplets=tod,
                boxes=boxes_L,
                LVGroups=L_VGroups
            )

        
            
class Bac2024Sujet0Exo5Question3TreesGPT(Scene):
    def construct(self):
        msg1 = "Bac 2024 Amérique du Nord 21 Mai 2024"
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
            (0, 1), (0, 2), (0, 3), (0, 4),
            (1, 5), (1, 6), (1, 7),
            (2, 8), (2, 9), (2, 10),
            (3, 11), (3, 12), (3, 13),
            (4, 14), (4, 15), (4, 16),
            (5, 17), (5, 18),
            (6, 19), (6, 20),
            (7, 21), (7, 22),
            (8, 23), (8, 24),
            (9, 25), (9, 26),
            (10, 27), (10, 28),
            (11, 29), (11, 30),
            (12, 31), (12, 32),
            (13, 33), (13, 34),
            (14, 35), (14, 36),
            (15, 37), (15, 38),
            (16, 39), (16, 40),
        ]

        true_labels = {
            0: "S",
            1: "4", 2: "3", 3: "2", 4: "1",
            5: "3", 6: "2", 7: "1",
            8: "2", 9: "1", 10: "4",
            11: "1", 12: "4", 13: "3",
            14: "4", 15: "3", 16: "2",
            17: "2", 18: "1",
            19: "1", 20: "3",
            21: "3", 22: "2",
            23: "1", 24: "4",
            25: "4", 26: "2",
            27: "2", 28: "1",
            29: "4", 30: "3",
            31: "3", 32: "1",
            33: "1", 34: "4",
            35: "3", 36: "2",
            37: "2", 38: "4",
            39: "4", 40: "3"
        }

        color_values = {
            "S": {"color": YELLOW},
            "1": {"color": BLUE},
            "2": {"color": WHITE},
            "3": {"color": RED},
            "4": {"color": PURPLE}
        }

        vertices_colors = {i: color_values[true_labels[i]] for i in range(41)}

        edges_colors = {
            edge: {"stroke_color": color_values[true_labels[edge[1]]]["color"]}
            for edge in edges
        }

        g = Graph(
            vertices, edges, layout="tree", root_vertex=0,
            layout_scale=6, labels=true_labels, 
            edge_config=edges_colors,
            vertex_config=vertices_colors,
            layout_config={"vertex_spacing": (0.75, 1.75)},
        )

        self.play(
            FadeOut(genVGroup),
            Create(g.next_to(generalize, 0.25 * DOWN).scale(0.75)),
            g.animate.shift(UP)
        )
        self.wait(2)

        T = [
            (4, 16, 40), (4, 16, 39), (4, 15, 38), (4, 15, 37),
            (4, 14, 36), (4, 14, 35), (3, 13, 34), (3, 13, 33),
            (3, 12, 32), (3, 12, 31), (3, 11, 30), (3, 11, 29),
            (2, 10, 28), (2, 10, 27), (2, 9, 26), (2, 9, 25),
            (2, 8, 24), (2, 8, 23), (1, 7, 22), (1, 7, 21),
            (1, 6, 20), (1, 6, 19), (1, 5, 18), (1, 5, 17)
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
            [g[i] for i in range(40, 16, -1)],
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

        L_VGroups = [VGroup(*L_i) for L_i in L]
        boxes_L = [
            SurroundingRectangle(
                VGroup(*L_i),
                color=GREEN,
                corner_radius=0.2
            ) for L_i in L
        ]

        def fadeout_doubles(self, boxes, lists):
            for i in range(3):
                self.play(
                    *[Write(b) for b in [boxes[i], boxes[i + 3]]],
                )
                self.wait()

                self.play(
                    ReplacementTransform(boxes[i + 3], boxes[i]),
                    *[FadeOut(o) for o in lists[i + 3]],
                    Unwrite(boxes[i]),
                )
                self.wait()

        blocks = [VGroup(*L_VGroups[i:i + 6]) for i in range(0, 24, 6)]
        block_boxes = [SurroundingRectangle(b) for b in blocks]

        subtrees = [
            VGroup(
                g[4], g[16], g[15], g[14], g[40], g[39],
                g[38], g[37], g[36], g[35]
            ),
            VGroup(
                g[3], g[13], g[12], g[11], g[34], g[33],
                g[32], g[31], g[30], g[29]
            ),
            VGroup(
                g[2], g[10], g[9], g[8], g[28], g[27],
                g[26], g[25], g[24], g[23]
            ),
            VGroup(
                g[1], g[7], g[6], g[5], g[22], g[21],
                g[20], g[19], g[18], g[17]
            )
        ]

        subtrees_boxes = [
            SurroundingRectangle(subtree) for subtree in subtrees
        ]

        self.play(
            *[Write(o) for o in [block_boxes[0], subtrees_boxes[0]]]
        )
        self.wait()
        fadeout_doubles(self, boxes=boxes_L, lists=L)

        for i in range(3):
            self.play(
                ReplacementTransform(block_boxes[i], block_boxes[i + 1]),
                ReplacementTransform(subtrees_boxes[i], subtrees_boxes[i + 1])
            )
            self.wait()
            fadeout_doubles(self, boxes=boxes_L[(i + 1) * 6:], lists=L[(i + 1) * 6:])

        self.wait()
        
        
        
        
class Bac2024Sujet0Exo5Question3Formule(Scene):
    def construct(self):
        msg1 = "Bac 2024 Amérique du Nord 21 Mai 2024"
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
        msg1 = "Bac 2024 Amérique du Nord 21 Mai 2024"
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
            r"Le mot ordonnée indique simplement qu'on tient compte de ",
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
        msg1 = "Bac 2024 Amérique du Nord 21 Mai 2024"
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
        msg1 = "Bac 2024 Amérique du Nord 21 Mai 2024"
        title5 = Title(f"{msg1}")
        self.add(title5.scale(1))
        self.wait(2)

        

        question5 = Title("Question 5").scale(0.55)
        q5_txt = [
            r"5. On effectue \(n\) lancers d'une pièce de monnaie équilibrée. ",
            r"Le résultat d'un lancer est pile ou face.",
            r"On considère la liste ordonnées des \(n\) résultats.",
            r"Quelle est la probabilité d'obtenir au plus deux fois pile dans "
            r"cette liste ?"
        ]

        q5 = [Tex(r).scale(0.55) for r in q5_txt]
        q5VGroup = VGroup(*q5)
            
        disp_tex_list(self, 
            previous_mobj=None,
            tex_list=q5,
            next2obj=title5,
            direction=DOWN
        )
        
        a = r"a. \(\dfrac{n(n - 1)}{2}\)"
        b = r"b. \(\dfrac{n(n - 1)}{2}\times\left(\dfrac{1}{2}\right)^n\)"
        c = r"c. \(1 + n + \dfrac{n(n - 1)}{2}\)"
        d = r"d. \(\left(1 + n + \dfrac{n(n - 1)}{2}\right)\times"
        d += r"\left(\dfrac{1}{2}\right)^n\)"
        
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
        sol_d = ent[3]
        box_d = SurroundingRectangle(sol_d)
        solution5 = Title("Réponse d")
        self.play(
            ReplacementTransform(attention_rep, solution5),
            Write(box_d)
        )
        self.wait()

        
        explanation = Title("Explications")
        self.play(
            ReplacementTransform(solution5, explanation),
            Unwrite(box_d)
        )
        self.wait()
        
        exp_d = [
            r"Chaque lancer d'une pièce suit une loi de Bernoulli.",
            r"Les lancers sont indépendants.",
            r"Soit \(X\) la variable aléatoire qui compte le nombre de pile.",
            r"\(X\) suit une loi binomiale de paramètres "
            r"\(\left(n ; \dfrac{1}{2}\right)\).",
            r"La probabilité cherchée est : \(P(X\leqslant 2)\).",
            r"Soit \(P(X = 0) + P(X = 1) + P(X = 2)\).",
            r"\(P(X\leqslant 2) = \dfrac{1}{2^n}\left(\binom{n}{0} + "
            r"\binom{n}{1} + \binom{n}{2}\right)\)",
            r"D'où le résultat.",
            r"\(P(X\leqslant 2) = \left(1 + n + \dfrac{n(n - 1)}{2}\right)"
            r"\times\left(\dfrac{1}{2}\right)^n\)"
            
        ]

        d_res = [Tex(r).scale(0.6) for r in exp_d]

        full_txt = VGroup(q5VGroup, m1)
        
        disp_tex_list(self, 
            previous_mobj=full_txt,
            tex_list=d_res,
            next2obj=title5,
            direction=DOWN
        )
        


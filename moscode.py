import streamlit as st
from streamlit_option_menu import option_menu
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw
from IPython.display import display

def integral(f,a,b,n=10000):
  return np.sum(f(np.linspace(a,b,n+1))) * (b-a)/(n+1)

def square(x):
  return x/x

def m(f, a, b, c, n=10000):
  def mom(x):
    return f(x)*(x-a)
  return integral(mom, b, c, n)

def mo(x):
  return (x-1)

def values(f1,f2,f3,f4,a,b,length,G,I):
  p = 0
  q = 0
  r2 = 0

  for i in f1:
      p += i[0]

  for i in f2:
      p += i[0] * (i[1] - a)
      q += i[0]

  for i in f3:
      def f(x):
          return i[0]*x**0
      p += m(f, a, i[1], i[2], n=10000)
      q += integral(f, i[1], i[2], n=10000)

  for i in f4:
      def f(x):
          return i[0]/(i[2]-i[1])*(x-i[1])
      p += m(f, a, i[1], i[2], n=10000)
      q += integral(f, i[1], i[2], n=10000)

  r2 = p/(a-b)
  r1 = -q - r2

  f2.extend([[r1,a],[r2,b]])
  f1.sort(key = lambda x: x[1])
  f2.sort(key = lambda x: x[1])
  f3.sort(key = lambda x: x[1])
  f4.sort(key = lambda x: x[1])
  l = np.linspace(0, length, 1001)
  dl = l[1]-l[0]
  i1 = i2 = i3 = i4 = -1
  l1 = len(f1); l2 = len(f2); l3 = len(f3); l4 = len(f4)
  arr = [2, 3, 4]
  v = 0
  V = []
  for j in l[:-1]:
      for i in arr:
          if i==2:
              if i2+1 == l2:
                  arr.remove(2)
              else:
                  if f2[i2+1][1]<=j:
                      v += f2[i2+1][0]
                      i2 += 1
                      if i2+1 == l2:
                          arr.remove(2)
                          break
          if i==3:
              if i3+1 == l3:
                  arr.remove(3)
                  break
              if f3[i3+1][1]<=j:
                  v += f3[i3+1][0]*dl
                  if f3[i3+1][2]<j:
                      i3 += 1
                  if i3+1 == l3:
                      arr.remove(3)
                      break
          if i==4:
              if i4+1 == l4:
                  arr.remove(4)
                  break
              if f4[i4+1][1]<=j:
                  t1 = f4[i4+1][0]; t2 = f4[i4+1][1]; t3 = f4[i4+1][2]
                  v += t1/(t3-t2)*(j-t2)*dl
                  if f4[i4+1][2]<j:
                      i4 += 1
                  if i4+1 == l4:
                      arr.remove(4)
                      break
      V.append(-v)
  V.append(-v)
  l = np.linspace(0, length, 1001)
  dl = l[1]-l[0]
  i1 = i2 = i3 = i4 = -1
  l1 = len(f1); l2 = len(f2); l3 = len(f3); l4 = len(f4)
  g1 = 0; g2 = 0; g3 = 0; g4 = 0
  arr = [1, 2,3,4]
  bm = 0
  BM = []
  for j in l[:-1]:
      for i in arr:
          if i==1:
              if i1+1 != l1 and f1[i1+1][1]<=j:
                  bm -= f1[i1+1][0]
                  if i1+1 != l1:
                      i1+=1
          if i==2:
              bm += g2*dl
              if i2+1 != l2 and f2[i2+1][1]<=j:
                  g2 += f2[i2+1][0]
                  if i2+1 != l2:
                      i2 += 1
          if i==3:
              bm += g3*dl
              if i3+1 != l3 and f3[i3+1][1]<=j:
                  g3 += f3[i3+1][0]*dl
                  if f3[i3+1][2]<j and i3+1 != l3:
                      i3 += 1
          if i==4:
              bm += g4*dl
              if i4+1 != l4 and f4[i4+1][1]<=j:
                  t1 = f4[i4+1][0]; t2 = f4[i4+1][1]; t3 = f4[i4+1][2]
                  g4 += t1/(t3-t2)*(j-t2)*dl
                  if f4[i4+1][2]<j and i4+1 != l4:
                      i4 += 1

      BM.append(bm)
  BM.append(bm)
  slope = []
  da = 0
  for i in BM:
    da += i*dl
    slope.append(da)
  deflection = []
  da = 0
  ai = 0; bi = 0
  for i in slope:
    da += i*dl
    deflection.append(da)
  for i in range(len(l)):
    if l[i]==a:
      ai = i
    if l[i] == b:
      bi = i
  c2 = (a*deflection[bi]-b*deflection[ai])/(b-a)
  c1 = (deflection[ai]-deflection[bi])/(b-a)
  for i in range(len(l)):
    deflection[i] += c1*l[i]+c2
    deflection[i] /= (G*I)
    slope[i] += c1
    slope[i] /= (G*I)
  return V,BM,slope,deflection

def draw_beam(l, support1, support2, f1, f2, f3, f4):
    image = Image.new("RGB", (400, 400), "pink")

    # Draw the beam
    draw = ImageDraw.Draw(image)
    rectangle_coords = [(50, 190), (350, 210)]
    draw.rectangle(rectangle_coords, outline="black", fill=(246, 167, 89), width=2)

    # Draw the supports
    X = [support1*300/l+50, support2*300/l+50]
    y = 210
    side = 30
    for x in X:
        draw.polygon([x, y, x-side*np.cos(np.pi/3), y+side*np.cos(np.pi/6), x+side*np.cos(np.pi/3), y+side*np.cos(np.pi/6)], fill=(174, 94, 14), outline='black', width=2)

    # Draw the point moments
    for i in f1:
        moment_location = i[1]*300/l+50
        bounding_box = (moment_location-25, 175, moment_location+25, 225)
        start_angle = -130
        end_angle = 130
        value = str(abs(i[0]))
        draw.arc(bounding_box, start=start_angle, end=end_angle, fill="black", width=3)
        draw.text([moment_location, 150], value, fill="black", font_size=20)
        if i[0]<0:
            draw.line([moment_location-16.07, 219.151, moment_location-16.07, 229.151], fill='black', width=3)
            draw.line([moment_location-16.07, 219.151, moment_location-6.07, 213.151], fill='black', width=3)
        else:
            draw.line([moment_location-16.07, 180.849, moment_location-6.07, 186.849], fill='black', width=3)
            draw.line([moment_location-16.07, 180.849, moment_location-16.07, 170.849], fill='black', width=3)

    # Draw the point forces
    for i in f2:
        load_location = i[1]*300/l+50
        value = str(abs(i[0]))
        draw.text([load_location, 130], value, fill="black", font_size=20)
        if i[0]<0:
            draw.line([load_location, 155, load_location, 190], fill='black', width=3)
            draw.line([load_location+0.5, 190, load_location+15*np.cos(np.pi/4), 190-15*np.sin(np.pi/4)], fill='black', width=3)
            draw.line([load_location+0.5, 190, load_location-15*np.cos(np.pi/4), 190-15*np.sin(np.pi/4)], fill='black', width=3)
        else:
            draw.line([load_location, 155, load_location, 190], fill='black', width=3)
            draw.line([load_location+0.5, 155, load_location+15*np.cos(np.pi/4), 155+15*np.sin(np.pi/4)], fill='black', width=3)
            draw.line([load_location+0.5, 155, load_location-15*np.cos(np.pi/4), 155+15*np.sin(np.pi/4)], fill='black', width=3)

    # Draw the constant force profile
    for i in f3:
        load_start_location = i[1]*300/l+50
        load_end_location = i[2]*300/l+50
        value = str(abs(i[0]))
        draw.rectangle([(load_start_location, 155), (load_end_location, 190)], outline="black", fill=(163, 163, 163, 40), width=2)
        draw.text([(load_end_location+load_start_location)/2, 130], value, fill="black", font_size=20)
        if i[0]<0:
            draw.line([load_start_location+0.5, 190, load_start_location+15*np.cos(np.pi/4), 190-15*np.sin(np.pi/4)], fill='black', width=3)
            draw.line([load_start_location+0.5, 190, load_start_location-15*np.cos(np.pi/4), 190-15*np.sin(np.pi/4)], fill='black', width=3)
            draw.line([load_end_location+0.5, 190, load_end_location+15*np.cos(np.pi/4), 190-15*np.sin(np.pi/4)], fill='black', width=3)
            draw.line([load_end_location+0.5, 190, load_end_location-15*np.cos(np.pi/4), 190-15*np.sin(np.pi/4)], fill='black', width=3)
        else:
            draw.line([load_start_location+0.5, 155, load_start_location+15*np.cos(np.pi/4), 155+15*np.sin(np.pi/4)], fill='black', width=3)
            draw.line([load_start_location+0.5, 155, load_start_location-15*np.cos(np.pi/4), 155+15*np.sin(np.pi/4)], fill='black', width=3)
            draw.line([load_end_location+0.5, 155, load_end_location+15*np.cos(np.pi/4), 155+15*np.sin(np.pi/4)], fill='black', width=3)
            draw.line([load_end_location+0.5, 155, load_end_location-15*np.cos(np.pi/4), 155+15*np.sin(np.pi/4)], fill='black', width=3)

        # if load_end_location - load_start_location < 30:
        #     draw.line([load_start_location, 155, load_start_location, 190], fill='black', width=3)
        #     draw.line([load_start_location+0.5, 190, load_start_location+15*np.cos(np.pi/4), 190-15*np.sin(np.pi/4)], fill='black', width=3)
        #     draw.line([load_start_location+0.5, 190, load_start_location-15*np.cos(np.pi/4), 190-15*np.sin(np.pi/4)], fill='black', width=3)
        #     draw.line([load_end_location, 155, load_end_location, 190], fill='black', width=3)
        #     draw.line([load_end_location+0.5, 190, load_end_location+15*np.cos(np.pi/4), 190-15*np.sin(np.pi/4)], fill='black', width=3)
        #     draw.line([load_end_location+0.5, 190, load_end_location-15*np.cos(np.pi/4), 190-15*np.sin(np.pi/4)], fill='black', width=3)
        # else:
        #     draw.line([load_start_location, 155, load_start_location, 190], fill='black', width=3)
        #     draw.line([load_start_location+0.5, 190, load_start_location+15*np.cos(np.pi/4), 190-15*np.sin(np.pi/4)], fill='black', width=3)
        #     draw.line([load_start_location+0.5, 190, load_start_location-15*np.cos(np.pi/4), 190-15*np.sin(np.pi/4)], fill='black', width=3)
        #     draw.line([load_end_location, 155, load_end_location, 190], fill='black', width=3)
        #     draw.line([load_end_location+0.5, 190, load_end_location+15*np.cos(np.pi/4), 190-15*np.sin(np.pi/4)], fill='black', width=3)
        #     draw.line([load_end_location+0.5, 190, load_end_location-15*np.cos(np.pi/4), 190-15*np.sin(np.pi/4)], fill='black', width=3)
        #     n = abs(load_end_location - load_start_location)//30
        #     for j in range(n):
        #         draw.line([load_start_location+30*n, 155, load_start_location+30*n, 190], fill='black', width=3)
        #         draw.line([load_start_location+30*n+0.5, 190, load_start_location+30*n+15*np.cos(np.pi/4), 190-15*np.sin(np.pi/4)], fill='black', width=3)
        #         draw.line([load_start_location+30*n+0.5, 190, load_start_location+30*n-15*np.cos(np.pi/4), 190-15*np.sin(np.pi/4)], fill='black', width=3)


    # Draw the triangular force profile
    for i in f4:
        load_start_location = i[1]*300/l+50
        load_end_location = i[2]*300/l+50
        slope = 55/(load_end_location-load_start_location)
        value = str(abs(i[0]))
        draw.polygon([load_start_location, 190, load_end_location, 190-slope*(load_end_location-load_start_location), load_end_location, 190], outline="black", fill=(163, 163, 163, 40), width=2)
        draw.text([load_end_location, 115], value, fill="black", font_size=20)
        if i[0]<0:
            draw.line([load_end_location+0.5, 190, load_end_location+15*np.cos(np.pi/4), 190-15*np.sin(np.pi/4)], fill='black', width=3)
            draw.line([load_end_location+0.5, 190, load_end_location-15*np.cos(np.pi/4), 190-15*np.sin(np.pi/4)], fill='black', width=3)
        else:
            draw.line([load_end_location+0.5, 190, load_end_location+15*np.cos(np.pi/4), 155+15*np.sin(np.pi/4)], fill='black', width=3)
            draw.line([load_end_location+0.5, 190, load_end_location-15*np.cos(np.pi/4), 155+15*np.sin(np.pi/4)], fill='black', width=3)
        # if load_end_location - load_start_location < 30:
        #     # draw.line([load_start_location, 155, load_start_location, 190], fill='black', width=3)
        #     # draw.line([load_start_location+0.5, 190, load_start_location+15*np.cos(np.pi/4), 190-15*np.sin(np.pi/4)], fill='black', width=3)
        #     # draw.line([load_start_location+0.5, 190, load_start_location-15*np.cos(np.pi/4), 190-15*np.sin(np.pi/4)], fill='black', width=3)
        #     draw.line([load_end_location, 155-slope*(load_end_location-load_start_location), load_end_location, 190], fill='black', width=3)
        #     draw.line([load_end_location+0.5, 190, load_end_location+15*np.cos(np.pi/4), 190-15*np.sin(np.pi/4)], fill='black', width=3)
        #     draw.line([load_end_location+0.5, 190, load_end_location-15*np.cos(np.pi/4), 190-15*np.sin(np.pi/4)], fill='black', width=3)
        # else:
        #     # draw.line([load_start_location, 155, load_start_location, 190], fill='black', width=3)
        #     # draw.line([load_start_location+0.5, 190, load_start_location+15*np.cos(np.pi/4), 190-15*np.sin(np.pi/4)], fill='black', width=3)
        #     # draw.line([load_start_location+0.5, 190, load_start_location-15*np.cos(np.pi/4), 190-15*np.sin(np.pi/4)], fill='black', width=3)
        #     draw.line([load_end_location, 155-slope*(load_end_location-load_start_location), load_end_location, 190], fill='black', width=3)
        #     draw.line([load_end_location+0.5, 190, load_end_location+15*np.cos(np.pi/4), 190-15*np.sin(np.pi/4)], fill='black', width=3)
        #     draw.line([load_end_location+0.5, 190, load_end_location-15*np.cos(np.pi/4), 190-15*np.sin(np.pi/4)], fill='black', width=3)
        #     n = abs(load_end_location - load_start_location)//30
        #     for j in range(n):
        #         draw.line([load_start_location+30*n, 155-slope*30*n, load_start_location+30*n, 190], fill='black', width=3)
        #         draw.line([load_start_location+30*n+0.5, 190, load_start_location+30*n+15*np.cos(np.pi/4), 190-15*np.sin(np.pi/4)], fill='black', width=3)
        #         draw.line([load_start_location+30*n+0.5, 190, load_start_location+30*n-15*np.cos(np.pi/4), 190-15*np.sin(np.pi/4)], fill='black', width=3)
    return image

def main():
    ## session state
    if 'f1' not in st.session_state:
        st.session_state.f1 = []
    if 'f2' not in st.session_state:
        st.session_state.f2 = []
    if 'f3' not in st.session_state:
        st.session_state.f3 = []
    if 'f4' not in st.session_state:
        st.session_state.f4 = []
    if 'V' not in st.session_state:
        st.session_state.V = []
    if 'BM' not in st.session_state:
        st.session_state.BM = []
    if 'slope' not in st.session_state:
        st.session_state.slope = []
    if 'deflection' not in st.session_state:
        st.session_state.deflection = []
    if 'G' not in st.session_state:
        st.session_state.G = 0
    if 'I' not in st.session_state:
        st.session_state.I = 0

    ## layout
    col = st.columns((2, 1), gap='medium')
    with col[0]:

        ## beam length
        st.subheader("Enter beam length:")
        beam_length = st.slider("meters:", min_value=0, max_value=100, value=50)
        "Beam Length:", beam_length,"m" 

        ## support location
        st.subheader("Enter supports location:")
        support_locations = st.slider("meters:", min_value=0, max_value=beam_length, value=[beam_length//4,3*beam_length//4])
        support_1 = support_locations[0]
        support_2 = support_locations[1]
        st.write("Support locations:", support_1, ",", support_2)

        ## load type
        st.subheader("Select load type:")
        load_types = ["Point Moment", "Point Force", "Constant Force Profile", "Triangular Force Profile"]
        load_type = option_menu("Load type:", load_types, orientation="horizontal") 

        if load_type == "Point Moment":
            moment_value = st.number_input("Enter moment value",step=1, key="point_moment_value")
            load_location = st.slider("meters:", min_value=0, max_value=beam_length, value=beam_length//2, key="point_moment_location")

        elif load_type == "Point Force":
            force_value = st.number_input("Enter force value",step=1, key="point_force_value")
            load_location = st.slider("meters:", min_value=0, max_value=beam_length, value=beam_length//2, key="point_force_location")

        elif load_type == "Constant Force Profile":
            w_value = st.number_input("Enter w value",step=1, key="constant_force_profile_value")
            load_range = st.slider("meters:", min_value=0, max_value=beam_length, value=[beam_length//4,3*beam_length//4], key="constant_force_profile_location")

        elif load_type == "Triangular Force Profile":
            w0_value = st.number_input("Enter w0 value",step=1, key="triangular_force_profile_value")
            load_range = st.slider("meters:", min_value=0, max_value=beam_length, value=[beam_length//4,3*beam_length//4], key="triangular_force_profile_location")

        add_load = st.button("Add load")
        if add_load:
            if load_type == "Point Moment":
                st.session_state.f1.append([moment_value,load_location])
                add_load = False

            elif load_type == "Point Force":
                st.session_state.f2.append([force_value,load_location])
                add_load = False

            elif load_type == "Constant Force Profile":  
                st.session_state.f3.append([w_value,load_range[0],load_range[1]])
                add_load = False

            elif load_type == "Triangular Force Profile":
                st.session_state.f4.append([w0_value,load_range[0],load_range[1]])
                add_load = False
                
        done = st.button("Done with Force")
        if done:
            V,BM,slope,deflection=values(st.session_state.f1,st.session_state.f2,st.session_state.f3,st.session_state.f4,support_1,support_2,beam_length,1,1)
            col2 = st.columns((3,3), gap='medium')

            fig1,ax1=plt.subplots()
            ax1.plot(V) # take value from backend
            st.write("Shear Force Diagram")
            st.pyplot(fig1, width=400)

            fig2,ax2=plt.subplots()
            ax2.plot(BM) # take value from backend
            st.write("Bending Moment Diagram")
            st.pyplot(fig2, width=400)


            fig4,ax4=plt.subplots()
            ax4.plot(deflection) # take value from backend
            st.write("Deflection of Beam")
            st.pyplot(fig4, width=400)

            fig3,ax3=plt.subplots()
            ax3.plot(slope) # take value from backend
            st.write("Slope of beam")
            st.pyplot(fig3, width=400)

    
    with col[1]:
        ## real time schematic
        image = draw_beam(beam_length, support_1, support_2, st.session_state.f1, st.session_state.f2, st.session_state.f3, st.session_state.f4)
        st.image(image, channels="RGB", width=400)

if __name__ == "__main__":
    main()


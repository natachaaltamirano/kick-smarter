import matplotlib.pyplot as plt
import seaborn as sns
plt.style.use('fivethirtyeight')

def plot_recomendation(num_perks,num_of_words_about,freq_bold_A,words_x_perk,num_pics,num_links):
    cate=["Funded","Unfunded","You"]

    plt.figure(figsize=(15, 15))

    plt.subplot(431)
    plt.bar([1,2,3],[9,0,0],color="g")
    plt.bar([1,2,3],[0,5,0],color="r")
    plt.bar([1,2,3],[0,0,num_perks],color="b")
    plt.xticks([1,2,3], cate, rotation="horizontal")
    plt.title("Number of Perks")


    plt.subplot(432) # equivalent to: plt.subplot(2, 2, 1)
    plt.bar([1,2,3],[501,0,0],color="g")
    plt.bar([1,2,3],[0,323,0],color="r")
    plt.bar([1,2,3],[0,0,num_of_words_about],color="b")
    plt.xticks([1,2,3], cate, rotation="horizontal")
    plt.title("Number of Words ")
    #plt.grid("false")



    plt.subplot(433) # equivalent to: plt.subplot(2, 2, 1)
    plt.bar([1,2,3],[5,0,0],color="g")
    plt.bar([1,2,3],[0,3.0,0],color="r")
    plt.bar([1,2,3],[0,0,freq_bold_A],color="b")
    plt.xticks([1,2,3], cate, rotation="horizontal")
    plt.title("Bold Words *")


    plt.subplot(434) # equivalent to: plt.subplot(2, 2, 1)
    plt.bar([1,2,3],[32,0,0],color="g")
    plt.bar([1,2,3],[0,23,0],color="r")
    plt.bar([1,2,3],[0,0,words_x_perk],color="b")
    plt.xticks([1,2,3], cate, rotation="horizontal")
    plt.title("Words per Perk")
    #plt.grid("false")

    plt.subplot(435) # equivalent to: plt.subplot(2, 2, 1)
    plt.bar([1,2,3],[5,0,0],color="g")
    plt.bar([1,2,3],[0,2,0],color="r")
    plt.bar([1,2,3],[0,0,num_pics],color="b")
    plt.xticks([1,2,3], cate, rotation="horizontal")
    plt.title("Number of Pictures")



    plt.subplot(4,3,6) # equivalent to: plt.subplot(2, 2, 1)
    plt.bar([1,2,3],[3,0,0],color="g")
    plt.bar([1,2,3],[0,1,0],color="r")
    plt.bar([1,2,3],[0,0,num_links],color="b")
    plt.xticks([1,2,3], cate, rotation="horizontal")
    plt.title("Number of Links")

    #plt.subplot(4,3,11) # equivalent to: plt.subplot(2, 2, 1)
    #plt.bar([1,2,3],[np.mean(features1_F["num_of_exclamation_P"]),0,0],color="g")
    #plt.bar([1,2,3],[0,np.mean(features1_UF["num_of_exclamation_P"]),0],color="r")
    #plt.bar([1,2,3],[0,0,ff["num_of_exclamation_P"]],color="b")
    #plt.xticks([1,2,3], cate, rotation="horizontal")
    #plt.title("num_of_exclamation_P")
    #plt.grid("false")
    plt.subplots_adjust(top = 0.99, bottom=0.01, hspace=0.3, wspace=0.4)

    #plt.subplot(4,3,12) # equivalent to: plt.subplot(2, 2, 1)
    #plt.bar([1,2,3],[np.mean(features1_F["num_of_sent_risk"]),0,0],color="g")
    #plt.bar([1,2,3],[0,np.mean(features1_UF["num_of_sent_risk"]),0],color="r")
    #plt.bar([1,2,3],[0,0,ff["num_of_sent_risk"]],color="b")
    #plt.xticks([1,2,3], cate, rotation="horizontal")
    #plt.title("num_of_sent_risk")

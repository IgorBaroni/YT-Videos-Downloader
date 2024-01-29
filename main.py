import flet as ft
from pytube import YouTube
import os 

def main(page: ft.Page):
    text = ft.Text("YouTube Videos Downloader", size=30)
    pb = ft.ProgressBar(width=400, color="green", bgcolor="#eeeeee")
    page.title = "YTV Downloader"

    def getVideoInfo(e):
        try:
            yt = YouTube(url.value)
            titulo = f"{yt.title} by {yt.author}"
            page.pubsub.send_all(titulo)
        except:
            page.pubsub.send_all("Video not found!")
        page.update()
            

    url = ft.TextField(width=500, label="URL", autofocus=True, on_change=getVideoInfo)


    dropdown = ft.Dropdown(
        width=160,
        label="Quality",
        options=[
            ft.dropdown.Option("MAX Resolution"),
            ft.dropdown.Option("MIN Resolution")
        ]
    )
    row = ft.Row([url, dropdown], spacing=30, alignment=ft.MainAxisAlignment.CENTER)
    videotitle = ft.Text("", size=20)

    def setVideoTitle(info):
        videotitle.value = info

        page.update()

    page.pubsub.subscribe(setVideoTitle)


    def close(e):
        popup.open = False,
        page.update()

    popup = ft.AlertDialog(
        open=False,
        modal=True,
        actions_alignment= ft.MainAxisAlignment.CENTER
    )
    def downloadVideo(e):
        page.dialog = popup 
        if len(url.value) > 24 and dropdown.value:
            popup.title=ft.Text("Downloading...", color="Green", text_align=ft.TextAlign.CENTER)
            popup.content = pb
            popup.actions = None
            popup.open = True
            page.update()

            current_folder = os.getcwd()
            yt = YouTube(url.value)
            

            if dropdown.value == "MAX Resolution":
                video = yt.streams.get_highest_resolution()
            elif dropdown.value == "MIN Resolution":
                video = yt.streams.get_lowest_resolution()

            video.download(output_path=current_folder+"/videos")
            popup.title=ft.Text("Video Downloaded!", color="Green")
            
        elif not(dropdown.value):
            popup.title=ft.Text("Select a Quality!", color="Red", text_align=ft.TextAlign.CENTER)
        else:
            popup.title=ft.Text("Enter a valid YouTube URL!", color="Red", text_align=ft.TextAlign.CENTER)
            
        popup.content = None
        popup.actions = [ft.ElevatedButton("Ok", on_click=close)]
        popup.open = True
        page.update()

    submit = ft.ElevatedButton("Download", on_click=downloadVideo)
    
    
    column = ft.Column(
        [text, row, submit, videotitle], 
        horizontal_alignment=ft.CrossAxisAlignment.CENTER, 
        width=100000, 
        spacing=25
    )

    page.add(column)


ft.app(main, view=ft.WEB_BROWSER)
import os
import shutil
import asyncio
import requests 
from astrbot.api.all import *
import jmcomic
from PIL import Image

@register("jmcomic_pdf", "Air", "私聊专属 JM PDF 直传", "1.0.0")
class JMComicPDFPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)
        self.base_mount_dir = "/AstrBot/data/jm_tmp"
        if not os.path.exists(self.base_mount_dir):
            os.makedirs(self.base_mount_dir, exist_ok=True)
            os.chmod(self.base_mount_dir, 0o777)

    @command("jm")
    async def fetch_comic(self, event: AstrMessageEvent, comic_id: str):
    # =================【安全护盾：白名单机制】=================
        # 将允许使用的 QQ 号写在这里，用英文双引号括起来，逗号隔开
        WHITELIST = ["朋友的QQ号1", "朋友的QQ号2"]
        
        # 获取发指令的人的 ID
        sender_id = event.get_sender_id()
        
        # 如果发消息的人不在白名单里
        if not any(qq in sender_id for qq in WHITELIST):
            # 强烈建议直接 return 装死！在陌生人眼里，它就是一个死号，根本不会引起注意。
            return
        if not comic_id.isdigit():
            yield event.plain_result("❌ 主人，ID 必须是纯数字。")
            return

        yield event.plain_result(f"⏳ 收到！开始为您下载 ID: {comic_id}...")

        work_dir = os.path.join(self.base_mount_dir, comic_id)
        if os.path.exists(work_dir):
            shutil.rmtree(work_dir, ignore_errors=True)
        os.makedirs(work_dir, exist_ok=True)
        os.chmod(work_dir, 0o777)

        try:
            option = jmcomic.JmOption.default()
            option.dir_rule.base_dir = work_dir
            await asyncio.to_thread(jmcomic.download_album, comic_id, option)

            images = []
            pdf_name = f"{comic_id}.pdf"
            pdf_path = os.path.join(work_dir, pdf_name)
            
            for root, dirs, files in os.walk(work_dir):
                valid_files = [f for f in files if f.lower().endswith(('.webp', '.jpg', '.jpeg', '.png'))]
                if valid_files:
                    valid_files.sort() 
                    for file in valid_files:
                        img_path = os.path.join(root, file)
                        try:
                            img = Image.open(img_path).convert('RGB')
                            images.append(img)
                        except: pass
                    break

            if images:
                images[0].save(pdf_path, "PDF", resolution=100.0, save_all=True, append_images=images[1:])

            if os.path.exists(pdf_path):
                yield event.plain_result("✅ PDF 缝合完毕，正在打包送往云端...")
                
                # 上传到完全匿名、免费的临时文件云端
                def upload_to_tmpfiles():
                    url = "https://tmpfiles.org/api/v1/upload"
                    with open(pdf_path, 'rb') as f:
                        response = requests.post(url, files={'file': f})
                    return response.json()

                upload_res = await asyncio.to_thread(upload_to_tmpfiles)
                
                if upload_res.get("status") == "success":
                    raw_url = upload_res["data"]["url"]
                    direct_url = raw_url.replace("tmpfiles.org/", "tmpfiles.org/dl/")
                    # 比如把点替换掉
                    safe_url = direct_url.replace(".", "。").replace("http://", "")
                    msg = f"请复制这段文字到浏览器，把句号改成点即可下载：\n{safe_url}"
                    
                    yield event.plain_result(msg)
                else:
                    yield event.plain_result("❌ 云端中转失败，请检查网络代理。")
                
                # 发送完毕，销毁本地证据
                shutil.rmtree(work_dir, ignore_errors=True)
            else:
                yield event.plain_result("❌ 逻辑走通了，但没找到生成的 PDF。")

        except Exception as e:
            yield event.plain_result(f"❌ 运行报错: {str(e)}")

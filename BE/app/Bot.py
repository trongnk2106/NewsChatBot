from langchain_community.llms import CTransformers
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_community.embeddings import GPT4AllEmbeddings
from langchain_community.vectorstores import FAISS
from accelerate import Accelerator
accelerator = Accelerator()

from langchain.text_splitter import RecursiveCharacterTextSplitter, CharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import GPT4AllEmbeddings
import re
# import sys
import sys
sys.path.append('../../MMIR/BE/Datapipeline')

# from DataPineLine.test import search
# from DataPineLine.model import Model

from MainSearch import search, full_textsearch



# Cau hinh
model_file = "models/vinallama-2.7b-chat_q5_0.gguf"
# vector_db_path = "vectorstores/db_faiss"



def create_db_from_text(raw_text):
    # raw_text = """Nhằm đáp ứng nhu cầu và thị hiếu của khách hàng về việc sở hữu số tài khoản đẹp, dễ nhớ, giúp tiết kiệm thời gian, mang đến sự thuận lợi trong giao dịch. Ngân hàng Sài Gòn – Hà Nội (SHB) tiếp tục cho ra mắt tài khoản số đẹp 9 số và 12 số với nhiều ưu đãi hấp dẫn.
    # Cụ thể, đối với tài khoản số đẹp 9 số, SHB miễn phí mở tài khoản số đẹp trị giá 880.000đ; giảm tới 80% phí mở tài khoản số đẹp trị giá từ 1,1 triệu đồng; phí mở tài khoản số đẹp siêu VIP chỉ còn 5,5 triệu đồng.
    # Đối với tài khoản số đẹp 12 số, SHB miễn 100% phí mở tài khoản số đẹp, khách hàng có thể lựa chọn tối đa toàn bộ dãy số của tài khoản. Đây là một trong những điểm ưu việt của tài khoản số đẹp SHB so với thị trường. Ngoài ra, khách hàng có thể lựa chọn số tài khoản trùng số điện thoại, ngày sinh, ngày đặc biệt, hoặc số phong thủy mang lại tài lộc cho khách hàng trong quá trình sử dụng.
    # Hiện nay, SHB đang cung cấp đến khách hàng 3 loại tài khoản số đẹp: 9 số, 10 số và 12 số. Cùng với sự tiện lợi khi giao dịch online mọi lúc mọi nơi qua dịch vụ Ngân hàng số, hạn chế rủi ro khi sử dụng tiền mặt, khách hàng còn được miễn phí chuyển khoản qua mobile App SHB, miễn phí quản lý và số dư tối thiểu khi sử dụng tài khoản số đẹp của SHB.
    # Ngoài kênh giao dịch tại quầy, khách hàng cũng dễ dàng mở tài khoản số đẹp trên ứng dụng SHB Mobile mà không cần hồ sơ thủ tục phức tạp.
    # Hướng mục tiêu trở thành ngân hàng số 1 về hiệu quả tại Việt Nam, ngân hàng bán lẻ hiện đại nhất và là ngân hàng số được yêu thích nhất tại Việt Nam, SHB sẽ tiếp tục nghiên cứu và cho ra mắt nhiều sản phẩm dịch vụ số ưu việt cùngchương trình ưu đãi hấp dẫn, mang đến cho khách hàng lợi ích và trải nghiệm tuyệt vời nhất.
    # Để biết thêm thông tin về chương trình, Quý khách vui lòng liên hệ các điểm giao dịch của SHB trên toàn quốc hoặc Hotline *6688"""
   
    # Chia nho van ban
    text_splitter = CharacterTextSplitter(
        separator=".",
        chunk_size=256,
        chunk_overlap=10,
        length_function=len
    )

    chunks = text_splitter.split_text(raw_text)

    # Embeding
    embedding_model = GPT4AllEmbeddings(model_file = "models/all-MiniLM-L6-v2-f16.gguf") # caau 1 vecto

    # Dua vao Faiss Vector DB
    db = FAISS.from_texts(texts=chunks, embedding=embedding_model) # dua cau vao emdding roi luu 
    # db.save_local(vector_db_path)
    return db # nparray moi hhan la 1 vector, so hang == so cau split van ban bang cach chia chunks nhu o tren


# Load LLM
def load_llm(model_file):
    config = {'max_new_tokens': 100, 'repetition_penalty': 1.1, 'temperature':0.1, 'gpu_layers':30}

    llm = CTransformers(
        model=model_file,
        model_type="llama",
        max_new_tokens=100,
        temperature=0.1,
        # n_gpu_layers=1,
        n_batch = 1,
        
        # gpu_layers=50,
        config=config
    )
    llm, config = accelerator.prepare(llm, config)
    return llm

# Tao prompt template
def creat_prompt(template):
    prompt = PromptTemplate(template = template, input_variables=["context", "question"])
    return prompt


# Tao simple chain
def create_qa_chain(prompt, llm, db):
    llm_chain = RetrievalQA.from_chain_type(
        llm = llm,
        chain_type= "stuff",
        retriever = db.as_retriever(search_kwargs = {"k":3}, max_tokens_limit=100),
        return_source_documents = False,
        chain_type_kwargs= {'prompt': prompt}
    )
    return llm_chain



# Read tu VectorDB
# def read_vectors_db():
#     # Embeding
#     embedding_model = GPT4AllEmbeddings(model_file="models/all-MiniLM-L6-v2-f16.gguf")
#     db = FAISS.load_local(vector_db_path, embedding_model)
#     return db
class Bot():

    @staticmethod
    def botchat(question, mode):
        import time
        
        start = time.time()
        
        template = """<|im_start|>system\nSử dụng thông tin sau đây để trả lời câu hỏi. Nếu bạn không biết câu trả lời, hãy nói không biết, đừng cố tạo ra câu trả lời\n
            {context}<|im_end|>\n<|im_start|>user\n{question}<|im_end|>\n<|im_start|>assistant"""
        prompt = creat_prompt(template)
        
        # question ='TP HCM - Căn hộ hai phòng ngủ đa năng (2PN+1) tại The Privia có thiết kế cửa sổ lớn trong mỗi phòng, kèm không gian phụ đa năng linh hoạt chuyển đổi mục đích sử dụng'
        if mode == 'Vector Search':
            search_result = search(question)['hits']['hits'][0]['_source']
            raw_text = search_result['paragraphs']
        if mode == 'Full Text Search':
            search_result = full_textsearch(question)['hits']['hits'][0]['_source']
            raw_text = search_result['paragraphs']
        
        # print(type(search_result['hits']['hits'][0]))
        # print(search_result['hits']['hits'][0]['_source'])

        
        # # Bat dau thu nghiem
        db = create_db_from_text(raw_text=raw_text)
        # db = read_vectors_db()
        llm = load_llm(model_file)

        #Tao Prompt
        

        llm_chain  =create_qa_chain(prompt, llm, db)

        # Chay cai chain
        
        response = llm_chain.invoke({"query": question})
        # print(response)
        
        response = re.sub(r'<\|\|>', '', response['result'])
        # print(response)
        # print(response)
        search_result['answer'] = ''.join(response.replace('user','').replace('assistant','').replace('im_start','').replace('im_end','').replace("<||>",'').split('.')[:-1])
        # print(search_result)
        
        end = time.time()
        
        # r
        
        # print(response)
        print(end - start)
        
        return search_result
    
    @staticmethod
    def search_(query, mode):
        if mode == 'Vector Search':
            result = search(query)['hits']['hits']
        if mode == 'Full Text Search':
            
            result = full_textsearch(query)['hits']['hits']
        return result
import pandas as pd
from django.shortcuts import render
from io import TextIOWrapper

# قائمة الطفرات والأنماط المرتبطة بها والأدوية الموصى بها
mutation_patterns = {
    'BRCA1': {
        'pattern': 'AGTCAGTC',  # نمط الطفرة BRCA1
        'drugs': ['Olaparib', 'Talazoparib'],
        'info': 'BRCA1 mutations are associated with an increased risk of breast and ovarian cancers.'
    },
    'TP53': {
        'pattern': 'CAGTCTGA',  # نمط الطفرة TP53
        'drugs': ['Atezolizumab', 'Nivolumab'],
        'info': 'TP53 is known as the guardian of the genome; its mutations lead to various cancers.'
    },
    'EGFR': {
        'pattern': 'ACTGACGA',  # نمط الطفرة EGFR
        'drugs': ['Erlotinib', 'Gefitinib', 'Osimertinib'],
        'info': 'EGFR mutations are common in non-small cell lung cancer and are targeted by specific therapies.'
    },
    'KRAS': {
        'pattern': 'GTACTGAC',  # نمط الطفرة KRAS
        'drugs': ['Selumetinib', 'Sotorasib'],
        'info': 'KRAS mutations are associated with pancreatic cancer and other malignancies.'
    },
    'PIK3CA': {
        'pattern': 'TGACTCAG',  # نمط الطفرة PIK3CA
        'drugs': ['Alpelisib'],
        'info': 'Mutations in PIK3CA are linked to breast cancer and are targets for therapy.'
    },
    'HRAS': {
        'pattern': 'CAGGTT',  # نمط الطفرة HRAS
        'drugs': ['Tipifarnib'],
        'info': 'HRAS mutations are commonly found in bladder and thyroid cancers.'
    },
    'NRAS': {
        'pattern': 'GTTTAC',  # نمط الطفرة NRAS
        'drugs': ['Binimetinib'],
        'info': 'NRAS mutations are found in melanoma and are a target for specific therapies.'
    },
    'BRAF': {
        'pattern': 'TACAC',  # نمط الطفرة BRAF
        'drugs': ['Vemurafenib', 'Dabrafenib'],
        'info': 'BRAF mutations are associated with melanoma and colorectal cancer.'
    },
    'ALK': {
        'pattern': 'ACGCG',  # نمط الطفرة ALK
        'drugs': ['Crizotinib', 'Alectinib'],
        'info': 'ALK gene rearrangements are found in non-small cell lung cancer.'
    },
    'MET': {
        'pattern': 'CATCG',  # نمط الطفرة MET
        'drugs': ['Crizotinib'],
        'info': 'MET mutations are implicated in several cancers, including lung and liver cancer.'
    },
}

# دالة لتحليل تسلسل الحمض النووي والبحث عن الطفرات
def analyze_dna_sequence(dna_sequence, detected_mutations):
    # البحث عن الأنماط في تسلسل الحمض النووي
    dna_sequence = dna_sequence.upper()  # تحويل التسلسل إلى أحرف كبيرة لتجاهل الحالة
    for mutation, info in mutation_patterns.items():
        if info['pattern'] in dna_sequence and mutation not in detected_mutations:
            # إضافة الطفرة إلى قائمة الطفرات المكتشفة إذا لم تكن مكررة
            detected_mutations.add(mutation)

    return detected_mutations

# دالة لتحليل الملف المرفوع من المستخدم
def analyze_dna_from_file(file):
    try:
        if file.name.endswith('.csv'):
            # محاولة قراءة الملف كملف CSV
            df = pd.read_csv(TextIOWrapper(file.file, encoding='utf-8'))
        elif file.name.endswith('.txt'):
            # قراءة الملف كملف نصي
            lines = file.read().decode('utf-8').splitlines()  # قراءة كل السطور
            df = pd.DataFrame(lines, columns=['sequence'])  # تحويل السطور إلى DataFrame
        else:
            return ["Error: Unsupported file format. Please upload CSV or TXT."]
    except Exception as e:
        return [f"Error reading file: {str(e)}"]

    # التحقق من وجود عمود 'sequence'
    if 'sequence' not in df.columns:
        return ["Error: The file does not contain a 'sequence' column."]

    # تخزين الطفرات المكتشفة بدون تكرار باستخدام set
    detected_mutations = set()

    # تحليل كل تسلسل
    for sequence in df['sequence']:
        detected_mutations = analyze_dna_sequence(sequence, detected_mutations)

    # إرجاع الأدوية الموصى بها للطفرات المكتشفة
    results = []
    for mutation in detected_mutations:
        drugs = mutation_patterns[mutation]['drugs']
        info = mutation_patterns[mutation]['info']
        results.append(f"Detected Mutation: {mutation}, Recommended Drugs: {', '.join(drugs)}, Info: {info}")

    # إذا لم يتم اكتشاف أي طفرات في كل التسلسلات
    if not results:
        return ["No mutations detected! 😊"]

    return results

# دالة عرض HTML
def dna_diagnosis(request):
    result = []
    
    if request.method == 'POST':
        dna_file = request.FILES.get('dna_file')  # استلام ملف الحمض النووي
        
        if dna_file:
            # تحليل البيانات
            result = analyze_dna_from_file(dna_file)
        else:
            result = ["Error: No file uploaded."]
    
    return render(request, 'genetics/dna_diagnosis.html', {'result': result})

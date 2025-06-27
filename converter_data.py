import json
from datetime import datetime

def converter_data_nascimento():
    """Converte a data de nascimento do formato US para BR"""
    try:
        # Carregar dados atuais
        with open('pacientes.json', 'r', encoding='utf-8') as f:
            pacientes = json.load(f)
        
        print("🔄 Convertendo datas de nascimento...")
        
        for paciente in pacientes:
            data_atual = paciente.get('data_nascimento', '')
            if data_atual and '-' in data_atual:  # Formato US (YYYY-MM-DD)
                try:
                    # Converter de YYYY-MM-DD para DD/MM/YYYY
                    data_obj = datetime.strptime(data_atual, '%Y-%m-%d')
                    data_br = data_obj.strftime('%d/%m/%Y')
                    paciente['data_nascimento'] = data_br
                    print(f"✅ {paciente['nome']}: {data_atual} → {data_br}")
                except ValueError:
                    print(f"⚠️ Erro ao converter data para {paciente['nome']}: {data_atual}")
            else:
                print(f"ℹ️ {paciente['nome']}: Data já no formato correto ou vazia")
        
        # Salvar dados convertidos
        with open('pacientes.json', 'w', encoding='utf-8') as f:
            json.dump(pacientes, f, ensure_ascii=False, indent=2)
        
        print("✅ Conversão concluída!")
        return True
        
    except Exception as e:
        print(f"❌ Erro durante a conversão: {e}")
        return False

if __name__ == "__main__":
    converter_data_nascimento() 
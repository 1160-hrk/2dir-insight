"""
data_loader.py - NMRデータ読み込み機能

様々なフォーマットの2次元NMRデータを読み込み、
統一されたデータ構造に変換します。
"""

import numpy as np
import pandas as pd
from pathlib import Path
from typing import Dict, Any, Optional, Union, Tuple
import json
import h5py


class DataLoader:
    """2次元NMRデータ読み込みクラス"""
    
    def __init__(self):
        self.supported_formats = ['.nmr', '.fid', '.dat', '.txt', '.csv', '.h5']
        self.current_data = None
        self.metadata = {}
    
    def load_data(self, file_path: Union[str, Path]) -> Dict[str, Any]:
        """
        データファイルを読み込み
        
        Args:
            file_path: データファイルのパス
            
        Returns:
            読み込まれたデータとメタデータを含む辞書
        """
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"ファイルが見つかりません: {file_path}")
        
        if file_path.suffix not in self.supported_formats:
            raise ValueError(f"サポートされていないファイル形式: {file_path.suffix}")
        
        # ファイル形式に応じて適切なローダーを呼び出し
        if file_path.suffix == '.h5':
            return self._load_hdf5(file_path)
        elif file_path.suffix in ['.txt', '.dat']:
            return self._load_text_format(file_path)
        elif file_path.suffix == '.csv':
            return self._load_csv(file_path)
        elif file_path.suffix in ['.nmr', '.fid']:
            return self._load_nmr_format(file_path)
        else:
            raise NotImplementedError(f"ローダーが未実装: {file_path.suffix}")
    
    def _load_hdf5(self, file_path: Path) -> Dict[str, Any]:
        """HDF5形式のデータを読み込み"""
        with h5py.File(file_path, 'r') as f:
            data = {
                'spectrum': np.array(f['spectrum']),
                'frequencies_f1': np.array(f['frequencies_f1']),
                'frequencies_f2': np.array(f['frequencies_f2']),
                'metadata': dict(f.attrs)
            }
        return data
    
    def _load_text_format(self, file_path: Path) -> Dict[str, Any]:
        """テキスト形式のデータを読み込み"""
        try:
            # データ部分を読み込み
            data_matrix = np.loadtxt(file_path)
            
            # メタデータファイルがあるかチェック
            metadata_file = file_path.with_suffix('.json')
            metadata = {}
            if metadata_file.exists():
                with open(metadata_file, 'r') as f:
                    metadata = json.load(f)
            
            # デフォルトの周波数軸を生成
            f1_points, f2_points = data_matrix.shape
            freq_f1 = np.linspace(0, 12, f1_points)  # デフォルト12ppm
            freq_f2 = np.linspace(0, 12, f2_points)
            
            return {
                'spectrum': data_matrix,
                'frequencies_f1': freq_f1,
                'frequencies_f2': freq_f2,
                'metadata': metadata
            }
            
        except Exception as e:
            raise ValueError(f"テキストファイルの読み込みに失敗: {e}")
    
    def _load_csv(self, file_path: Path) -> Dict[str, Any]:
        """CSV形式のデータを読み込み"""
        try:
            df = pd.read_csv(file_path, index_col=0)
            data_matrix = df.values
            
            # 軸の情報を取得
            freq_f1 = df.index.values.astype(float)
            freq_f2 = df.columns.values.astype(float)
            
            metadata = {
                'file_format': 'csv',
                'original_file': str(file_path),
                'data_shape': data_matrix.shape
            }
            
            return {
                'spectrum': data_matrix,
                'frequencies_f1': freq_f1,
                'frequencies_f2': freq_f2,
                'metadata': metadata
            }
            
        except Exception as e:
            raise ValueError(f"CSVファイルの読み込みに失敗: {e}")
    
    def _load_nmr_format(self, file_path: Path) -> Dict[str, Any]:
        """NMR固有フォーマットのデータを読み込み"""
        # この部分は実際のNMRデータ形式に応じて実装
        # nmrglueライブラリを使用する場合の例
        
        try:
            # プレースホルダー実装
            # 実際にはnmrglueやその他のライブラリを使用
            metadata = {
                'file_format': 'nmr',
                'original_file': str(file_path),
                'note': 'NMR format loader needs implementation'
            }
            
            # ダミーデータ（実装時に置き換え）
            spectrum = np.random.random((512, 1024))
            freq_f1 = np.linspace(0, 12, 512)
            freq_f2 = np.linspace(0, 12, 1024)
            
            return {
                'spectrum': spectrum,
                'frequencies_f1': freq_f1,
                'frequencies_f2': freq_f2,
                'metadata': metadata
            }
            
        except Exception as e:
            raise ValueError(f"NMRファイルの読み込みに失敗: {e}")
    
    def save_data(self, data: Dict[str, Any], output_path: Union[str, Path], 
                  format: str = 'h5') -> None:
        """
        データを指定形式で保存
        
        Args:
            data: 保存するデータ
            output_path: 出力ファイルパス
            format: 出力形式 ('h5', 'csv', 'txt')
        """
        output_path = Path(output_path)
        
        if format == 'h5':
            self._save_hdf5(data, output_path)
        elif format == 'csv':
            self._save_csv(data, output_path)
        elif format == 'txt':
            self._save_text(data, output_path)
        else:
            raise ValueError(f"サポートされていない出力形式: {format}")
    
    def _save_hdf5(self, data: Dict[str, Any], output_path: Path) -> None:
        """HDF5形式で保存"""
        with h5py.File(output_path, 'w') as f:
            f.create_dataset('spectrum', data=data['spectrum'])
            f.create_dataset('frequencies_f1', data=data['frequencies_f1'])
            f.create_dataset('frequencies_f2', data=data['frequencies_f2'])
            
            # メタデータを属性として保存
            for key, value in data['metadata'].items():
                f.attrs[key] = value
    
    def _save_csv(self, data: Dict[str, Any], output_path: Path) -> None:
        """CSV形式で保存"""
        df = pd.DataFrame(
            data['spectrum'],
            index=data['frequencies_f1'],
            columns=data['frequencies_f2']
        )
        df.to_csv(output_path)
    
    def _save_text(self, data: Dict[str, Any], output_path: Path) -> None:
        """テキスト形式で保存"""
        np.savetxt(output_path, data['spectrum'])
        
        # メタデータを別ファイルで保存
        metadata_path = output_path.with_suffix('.json')
        with open(metadata_path, 'w') as f:
            json.dump(data['metadata'], f, indent=2)
    
    def get_data_info(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """データの基本情報を取得"""
        spectrum = data['spectrum']
        return {
            'shape': spectrum.shape,
            'dtype': str(spectrum.dtype),
            'min_value': float(np.min(spectrum)),
            'max_value': float(np.max(spectrum)),
            'mean_value': float(np.mean(spectrum)),
            'std_value': float(np.std(spectrum)),
            'frequency_range_f1': (
                float(np.min(data['frequencies_f1'])),
                float(np.max(data['frequencies_f1']))
            ),
            'frequency_range_f2': (
                float(np.min(data['frequencies_f2'])),
                float(np.max(data['frequencies_f2']))
            ),
            'metadata': data['metadata']
        } 
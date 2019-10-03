import streamlit as st
from chembl_webresource_client.new_client import new_client
import pandas as pd

from rdkit import Chem
from rdkit.Chem import Draw
from rdkit.Chem import PandasTools
from rdkit.Chem import AllChem
from rdkit.Chem import rdFingerprintGenerator
from rdkit import DataStructs

from sklearn.manifold import TSNE
from IPython.display import SVG
from rdkit.Chem import rdDepictor
from rdkit.Chem.Draw import rdMolDraw2D
from rdkit.Chem.PandasTools import ChangeMoleculeRendering

import json
from bokeh.plotting import figure, show, output_notebook, ColumnDataSource
from bokeh.models import HoverTool
from bokeh.transform import factor_cmap
from bokeh.plotting import figure, output_file, save

# @st.cache
# def get_data():
#     molecule = new_client.molecule
#     approved_drugs = molecule.filter(max_phase=4)
#     small_molecule_drugs = [x for x in approved_drugs if x['molecule_type'] == 'Small molecule']
    
#     struct_list = [(x['pref_name'], x['molecule_chembl_id'],x['molecule_structures'])for x in small_molecule_drugs if x]
#     smiles_list = [(a,b,c['canonical_smiles']) for (a,b,c) in struct_list if c]
#     smiles_df = pd.DataFrame(smiles_list)
#     smiles_df.columns = ['Name','ChEMBL_ID','SMILES']
#     return smiles_df

# functions

@st.cache
def get_data(file_name):
    file = pd.read_csv(f'data/{file_name}.csv')    
    return file

def moltoimage(smiles):
    mol = Chem.MolFromSmiles(smiles)
    return Chem.Draw.MolToImage(mol, size=(600,300))

def mol_formula(smiles):
    mol = Chem.MolFromSmiles(smiles)
    return Chem.rdMolDescriptors.CalcMolFormula(mol)

def _prepareMol(mol,kekulize):
    mc = Chem.Mol(mol.ToBinary())
    if kekulize:
        try:
            Chem.Kekulize(mc)
        except:
            mc = Chem.Mol(mol.ToBinary())
    if not mc.GetNumConformers():
        rdDepictor.Compute2DCoords(mc)
    return mc

def moltosvg(mol,molSize=(450,200),kekulize=True,drawer=None,**kwargs):
    mc = _prepareMol(mol,kekulize)
    if drawer is None:
        drawer = rdMolDraw2D.MolDraw2DSVG(molSize[0],molSize[1])
    drawer.DrawMolecule(mc,**kwargs)
    drawer.FinishDrawing()
    svg = drawer.GetDrawingText()
    return SVG(svg.replace('svg:',''))

@st.cache
def tsne_cluster(df):
    mols = [Chem.MolFromSmiles(s) for s in df.SMILES]
    ECFP4_fps = [AllChem.GetMorganFingerprintAsBitVect(x,2) for x in mols]
    tsne = TSNE(random_state=0).fit_transform(ECFP4_fps)
    imol = [moltosvg(m).data for m in mols]
    return tsne, imol
    
    


# app
    
file_name = 'small_molecule_drug'    

data_load_state = st.text('Loading data...')
data = get_data(file_name)
data_load_state.text('Loading data...done!')

#check the data
if st.sidebar.checkbox('Show All Drugs'):
    st.subheader('All Drugs')
    st.dataframe(data)
    



#bokeh

tsne, svgs = tsne_cluster(data)

ChangeMoleculeRendering(renderer='PNG')


source = ColumnDataSource(data=dict(x=tsne[:,0], y=tsne[:,1], desc= data.Name, 
                                    svgs=svgs))

hover = HoverTool(tooltips="""
    <div>
        <div>@svgs{safe}
        </div>
        <div>
            <span style="font-size: 17px; font-weight: bold;">@desc</span>
        </div>
    </div>
    """
)
interactive_map = figure(plot_width=1000, plot_height=1000, tools=['reset,box_zoom,wheel_zoom,zoom_in,zoom_out,pan',hover],
           title="Small Molecule Drug (ECFP4)")



interactive_map.circle('x', 'y', size=5, source=source, fill_alpha=0.2);


# Show chemical space
if st.sidebar.checkbox('Show the chemical space'):
    st.bokeh_chart(interactive_map)


# select one compound
selected_name = st.sidebar.selectbox(
    'Select by Name',
     data['Name'])

'Selected Drug: ', 
data.loc[data['Name'] == selected_name]

# show structure
# TODO: improve image quility https://iwatobipen.wordpress.com/2017/11/03/draw-high-quality-molecular-image-in-rdkit-rdkit/
st.write(f'Structure:')
st.image(moltoimage(data.loc[data['Name'] == selected_name]['SMILES'].values[0]), caption = selected_name, use_column_width=True)

#  show properites

st.write('Molecular Fomula: ', mol_formula(data.loc[data['Name'] == selected_name]['SMILES'].values[0]))

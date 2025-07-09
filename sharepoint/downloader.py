import os
import pathlib
from pydantic import BaseModel
import msal
import requests

class SharePointDownloader(BaseModel):
    """
    A class to handle downloading files from SharePoint.
    """
    tenant_id: str
    client_id: str
    client_secret: str
    site_host: str
    site_path: str
    src_folder: str
    dest_folder: pathlib.Path
    graph_root: str

    @classmethod
    def from_env(cls):
        """
        Create an instance of SharePointDownloader using environment variables.
        """
        tenant_id = os.getenv("SHAREPOINT_TENANT_ID")
        if not tenant_id:
            raise ValueError("SHAREPOINT_TENANT_ID environment variable is not set.")
        client_id = os.getenv("SHAREPOINT_CLIENT_ID")
        if not client_id:
            raise ValueError("SHAREPOINT_CLIENT_ID environment variable is not set.")
        client_secret = os.getenv("SHAREPOINT_CLIENT_SECRET")
        if not client_secret:
            raise ValueError("SHAREPOINT_CLIENT_SECRET environment variable is not set.")
        site_host = os.getenv("SHAREPOINT_SITE_HOST")
        if not site_host:
            raise ValueError("SHAREPOINT_SITE_HOST environment variable is not set.")
        site_path = os.getenv("SHAREPOINT_SITE_PATH")
        if not site_path:
            raise ValueError("SHAREPOINT_SITE_PATH environment variable is not set.")
        src_folder = os.getenv("SHAREPOINT_SRC_FOLDER", "")
        if not src_folder:
            raise ValueError("SHAREPOINT_SRC_FOLDER environment variable is not set.")
        dest_folder = os.getenv("SHAREPOINT_DEST_FOLDER")
        if not dest_folder:
            raise ValueError("SHAREPOINT_DEST_FOLDER environment variable is not set.")

        return cls(
            tenant_id=tenant_id,
            client_id=client_id,
            client_secret=client_secret,
            site_host=site_host,
            site_path=site_path,
            src_folder=src_folder,
            dest_folder=pathlib.Path(dest_folder),
            graph_root="https://graph.microsoft.com/"
        )
    
    def get_access_token(self):
        """
        Get a Bearer token for SharePoint access.
        This method should be implemented to retrieve the access token using the client credentials.
        """
        authority = f"https://login.microsoftonline.com/{self.tenant_id}"
        app = msal.ConfidentialClientApplication(
            client_id=self.client_id,
            client_credential=self.client_secret,
            authority=authority
        )
        result = app.acquire_token_for_client(scopes=[f"{self.graph_root}/.default"])
        if "access_token" not in result:
            raise RuntimeError(f"Impossibile ottenere il token: {result.get('error_description')}")
        return result["access_token"]
    
    def graph_get(self, url: str, token: str, **params):
        headers = {"Authorization": f"Bearer {token}"}
        resp = requests.get(url, headers=headers, params=params, timeout=30)
        resp.raise_for_status()
        return resp.json()
    
    def list_all_files(self, drive_id: str, folder_id: str, token: str) -> list[dict]:
    # Ricorsivamente lista tutti i file sotto la cartella identificata da folder_id
        items = []
        url = f"{self.graph_root}/v1.0/drives/{drive_id}/items/{folder_id}/children"
        while url:
            response = self.graph_get(url, token)
            for item in response.get("value", []):
                if "folder" in item:
                    # è una cartella, ricorsione
                    items.extend(self.list_all_files(drive_id, item["id"], token))
                elif "file" in item:
                    items.append(item)
            url = response.get("@odata.nextLink")
        return items
    
    def download_file(self, item: dict, filename: pathlib.Path):
            download_url = item.get("@microsoft.graph.downloadUrl")
            if download_url:
                url = download_url 
                headers = {} 
            else:
                raise ValueError("Nessun URL di download disponibile per questo file.")

            with requests.get(url, headers=headers, stream=True, timeout=120) as r:
                r.raise_for_status()
                with open(filename, "wb") as f:
                    for chunk in r.iter_content(chunk_size=65536):
                        f.write(chunk)

    def download_all_files(self):
        """
        Download all files from the specified SharePoint folder.
        """
        token = self.get_access_token()
        site = self.graph_get(f"{self.graph_root}/v1.0/sites/{self.site_host}:{self.site_path}", token)
        site_id = site["id"]

        drives = self.graph_get(f"{self.graph_root}/v1.0/sites/{site_id}/drives", token)
        drive_id = next((d["id"] for d in drives["value"] if d["name"] == "Documents"), None)
        if not drive_id:
            raise RuntimeError("Drive 'Documents' non trovato.")

        target_url = f"{self.graph_root}/v1.0/drives/{drive_id}/root:/{self.src_folder}"
        target = self.graph_get(target_url, token, select="id,name")
        
        # Lista ricorsiva di tutti i file nella cartella e sottocartelle
        items = self.list_all_files(drive_id, target["id"], token)
        
        print(f"Trovati {len(items)} elementi")
        for itm in items:
            print(f" - {itm['name']} (file: {'file' in itm}, folder: {'folder' in itm})")
        
        self.dest_folder.mkdir(exist_ok=True)
        for itm in items:
            if "file" not in itm:            # ignora eventuali sottocartelle
                continue
            local_path = self.dest_folder / itm["name"]
            self.download_file(itm, local_path)

        print(f"\nDownload completato in '{self.dest_folder.resolve()}'")